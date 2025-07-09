import enum

class DeliveryState(enum.Enum):
    PARCEL_COLLECTED = "PARCEL_COLLECTED"
    TAKEN_OFF = "TAKEN_OFF"
    LANDED = "LANDED"
    CRASHED = "CRASHED"
    PARCEL_DELIVERED = "PARCEL_DELIVERED"

    def ongoing_states(self):
        return (self.TAKEN_OFF, self.PARCEL_COLLECTED, self.LANDED)
