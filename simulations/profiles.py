"""Lightweight device-type and client profiles using Fisher-weighted Z scoring.

The per-feature Fisher weights are learned offline by the simulation notebook and
remain fixed during deployment. Online adaptation updates only each client's
feature means, standard deviations, and threshold; no classifier retraining is
performed.
"""

import math


DEFAULT_STD_FLOOR = 0.1


def _prepare_feature_weights(feature_means, feature_weights):
    """Return non-negative weights aligned with the profile's feature order."""
    supplied = feature_weights or {}
    weights = {}

    for feature in feature_means:
        weight = float(supplied.get(feature, 1.0))
        if not math.isfinite(weight) or weight < 0.0:
            raise ValueError(
                f"Feature weight for {feature!r} must be finite and non-negative."
            )
        weights[feature] = weight

    if sum(weights.values()) <= 0.0:
        raise ValueError("At least one feature weight must be positive.")

    return weights


def _calculate_score(
    window_features,
    feature_means,
    feature_stds,
    feature_weights,
    std_floor,
):
    """Calculate the Fisher-weighted mean absolute Z score."""
    weighted_sum = 0.0
    total_weight = 0.0

    for feature, mean in feature_means.items():
        value = window_features.get(feature, mean)
        std = max(feature_stds.get(feature, std_floor), std_floor)
        weight = feature_weights[feature]
        weighted_sum += weight * abs(value - mean) / std
        total_weight += weight

    return weighted_sum / total_weight


def _anchored_statistics(client_profile, general_profile, anchor_strength):
    """Blend client statistics with the original device-type statistics."""
    if not 0.0 <= anchor_strength <= 1.0:
        raise ValueError("anchor_strength must be between 0 and 1.")

    means = {}
    stds = {}

    for feature in client_profile.feature_means:
        client_mean = client_profile.feature_means[feature]
        client_std = max(
            client_profile.feature_stds[feature],
            client_profile.std_floor,
        )
        general_mean = general_profile.feature_means[feature]
        general_std = max(
            general_profile.feature_stds[feature],
            general_profile.std_floor,
        )

        means[feature] = (
            (1.0 - anchor_strength) * client_mean
            + anchor_strength * general_mean
        )

        variance = (
            (1.0 - anchor_strength) * client_std**2
            + anchor_strength * general_std**2
            + anchor_strength
            * (1.0 - anchor_strength)
            * (client_mean - general_mean) ** 2
        )
        stds[feature] = math.sqrt(variance)

    return means, stds


class DeviceTypes:
    """Store the fixed general statistics and Fisher weights for one device type."""

    def __init__(
        self,
        device_type_name,
        feature_means,
        feature_stds,
        threshold,
        feature_weights=None,
        std_floor=DEFAULT_STD_FLOOR,
        scoring_config=None,
    ):
        self.device_type_name = device_type_name
        self.feature_means = feature_means.copy()
        self.feature_stds = feature_stds.copy()
        self.feature_weights = _prepare_feature_weights(
            self.feature_means,
            feature_weights,
        )
        self.threshold = float(threshold)
        self.std_floor = float(std_floor)
        self.window_count = 0

        # Retained only so older analysis code that inspects this attribute does
        # not fail. It is not used by Fisher-weighted Z scoring.
        self.scoring_config = dict(scoring_config or {})
        self.scoring_method = "fisher_weighted_z"

    def score_window(self, window_features):
        """Score one traffic window against this fixed device-type profile."""
        return _calculate_score(
            window_features,
            self.feature_means,
            self.feature_stds,
            self.feature_weights,
            self.std_floor,
        )

    def is_anomalous(self, score):
        """Return True when a score exceeds the profile threshold."""
        return score > self.threshold

    def get_profile(self):
        """Return a serializable summary of the fixed device-type profile."""
        return {
            "device_type_name": self.device_type_name,
            "scoring_method": self.scoring_method,
            "threshold": self.threshold,
            "window_count": self.window_count,
            "features_used": list(self.feature_means.keys()),
            "feature_weights": self.feature_weights.copy(),
        }


class ClientProfiles:
    """Store the adaptive statistics and fixed Fisher weights for one client."""

    def __init__(
        self,
        client_id,
        device_type_name,
        feature_means,
        feature_stds,
        threshold,
        feature_weights=None,
        std_floor=DEFAULT_STD_FLOOR,
        scoring_config=None,
    ):
        self.client_id = client_id
        self.device_type_name = device_type_name
        self.feature_means = feature_means.copy()
        self.feature_stds = feature_stds.copy()
        self.feature_weights = _prepare_feature_weights(
            self.feature_means,
            feature_weights,
        )
        self.threshold = float(threshold)
        self.std_floor = float(std_floor)
        self.window_count = 0
        self.scoring_config = dict(scoring_config or {})
        self.scoring_method = "adaptive_fisher_weighted_z"

    def score_window(
        self,
        window_features,
        general_profile=None,
        anchor_strength=0.0,
    ):
        """Score one window using the client profile, optionally anchored to its type."""
        feature_means = self.feature_means
        feature_stds = self.feature_stds

        if general_profile is not None and anchor_strength > 0.0:
            feature_means, feature_stds = _anchored_statistics(
                self,
                general_profile,
                anchor_strength,
            )

        return _calculate_score(
            window_features,
            feature_means,
            feature_stds,
            self.feature_weights,
            self.std_floor,
        )

    def is_anomalous(self, score):
        """Return True when a score exceeds the current client threshold."""
        return score > self.threshold

    def get_profile(self):
        """Return a serializable summary of the adaptive client profile."""
        return {
            "client_id": self.client_id,
            "device_type_name": self.device_type_name,
            "scoring_method": self.scoring_method,
            "threshold": self.threshold,
            "window_count": self.window_count,
            "features_used": list(self.feature_means.keys()),
            "feature_weights": self.feature_weights.copy(),
        }
