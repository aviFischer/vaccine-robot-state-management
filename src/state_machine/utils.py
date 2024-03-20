# defining range of webcam coordinates we tolerate shoulder in
ALLOWABLE_X_RANGE = (350, 400)
ALLOWABLE_Y_RANGE = (200, 400)

SCALING_FACTOR = 1
BIAS = 200

def verify_shoulder_location(location:tuple[float, float]):
    if(not location):
        return False
    if location[1] < ALLOWABLE_X_RANGE[0] or location[1] > ALLOWABLE_X_RANGE[1]:
        return False
    if location[0] < ALLOWABLE_Y_RANGE[0] or location[0] > ALLOWABLE_Y_RANGE[1]:
        return False
    return True

def webcam_to_gantry(location:tuple[float, float]):
    return location[1] * SCALING_FACTOR + BIAS
