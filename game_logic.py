import math
import arcade
from dataclasses import dataclass
from logging import getLogger

logger = getLogger(__name__)


@dataclass
class ImpulseVector:
    angle: float
    impulse: float


@dataclass
class Point2D:
    x: float = 0
    y: float = 0


def get_angle_radians(point_a: Point2D, point_b: Point2D) -> float:
    ### ---------------------- ###
    ### SU IMPLEMENTACION AQUI ###
    ### ---------------------- ###
    delta_x = point_b.x - point_a.x
    delta_y = point_b.y - point_a.y
    angle = math.atan2(delta_y, delta_x)
    logger.debug(f"Angle between points: {math.degrees(angle)} degrees")
    return angle
    # return 0.0


def get_distance(point_a: Point2D, point_b: Point2D) -> float:
    ### ---------------------- ###
    ### SU IMPLEMENTACION AQUI ###
    ### ---------------------- ###
    distance = math.sqrt((point_b.x - point_a.x) ** 2 + (point_b.y - point_a.y) ** 2)
    logger.debug(f"Distance between points: {distance}")
    return distance
    # return 0.0


def get_impulse_vector(start_point: Point2D, end_point: Point2D) -> ImpulseVector:
    ### ---------------------- ###
    ### SU IMPLEMENTACION AQUI ###
    ### ---------------------- ###
    angle = get_angle_radians(end_point, start_point)
    distance = get_distance(end_point, start_point)
    
    impulse_magnitude = distance
    logger.debug(f"Impulse Vector - Angle: {math.degrees(angle)} degrees, Impulse: {impulse_magnitude}")
    return ImpulseVector(angle, impulse_magnitude)
    # return ImpulseVector(0, 0)
