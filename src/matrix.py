from math import cos, sin, radians, pi, asin, degrees, atan2

from app_typing import Matrix, Vector


def get_matrix_XYZ(psi, th, phi):
    sin1, cos1 = sin(psi), cos(psi)
    sin2, cos2 = sin(th), cos(th)
    sin3, cos3 = sin(phi), cos(phi)
    return [
        [cos2 * cos3,   sin1 * sin2 * cos3 - cos1 * sin3,   cos1 * sin2 * cos3 + sin1 * sin3],
        [cos2 * sin3,   sin1 * sin2 * sin3 + cos1 * cos3,   cos1 * sin2 * sin3 - sin1 * cos3],
        [-sin2,         sin1 * cos2,                        cos1 * cos2],
    ]


def get_matrix_XZY(psi, th, phi):
    sin1, cos1 = sin(psi), cos(psi)
    sin2, cos2 = sin(th), cos(th)
    sin3, cos3 = sin(phi), cos(phi)
    return [
        [cos2 * cos3,   -cos3 * sin2 * cos1 + sin3 * sin1,  cos3 * sin2 * sin1 + sin3 * cos1],
        [sin2,          cos1 * cos2,                        -cos2 * sin1],
        [-sin3 * cos2,  sin3 * sin2 * cos1 + cos3 * sin1,   -sin3 * sin2 * sin1 + cos3 * cos1],
    ]


def get_angles_XZY_new(R):
    if not eq(abs(R[1][0]), 1):
        th1 = asin(R[1][0])
        th2 = pi - th1
        psi1 = atan2(-R[1][2] / cos(th1), R[1][1] / cos(th1))
        psi2 = atan2(-R[1][2] / cos(th2), R[1][1] / cos(th2))
        phi1 = atan2(-R[2][0] / cos(th1), R[0][0] / cos(th1))
        phi2 = atan2(-R[2][0] / cos(th2), R[0][0] / cos(th2))

        sol1 = (psi1, th1, phi1)
        sol2 = (psi2, th2, phi2)
        return sol1 if sum(map(abs, sol1)) < sum(map(abs, sol2)) else sol2
    else:
        phi = 0
        if eq(R[1][0], 1):
            th = pi / 2
            psi = atan2(R[2][1], R[2][2]) - phi
        else:
            th = -pi / 2
            psi = phi - atan2(R[0][2], R[0][1])
        return psi, th, phi


def transpose(a):
    n, m = len(a), len(a[0])
    b = [[None] * n for i in range(m)]
    for i in range(n):
        for j in range(m):
            b[i][j] = a[j][i]
    return b


def eq(c1, c2):
    return abs(c1 - c2) < 1e-6


def get_angles_deg(R):
    return tuple(map(degrees, get_angles(R)))


def get_angles(R: Matrix):
    if not eq(abs(R[2][0]), 1):
        th1 = -asin(R[2][0])
        th2 = pi - th1
        psi1 = atan2(R[2][1] / cos(th1), R[2][2] / cos(th1))
        psi2 = atan2(R[2][1] / cos(th2), R[2][2] / cos(th2))
        phi1 = atan2(R[1][0] / cos(th1), R[0][0] / cos(th1))
        phi2 = atan2(R[1][0] / cos(th2), R[0][0] / cos(th2))

        sol1 = (psi1, th1, phi1)
        sol2 = (psi2, th2, phi2)
        return sol1 if sum(map(abs, sol1)) < sum(map(abs, sol2)) else sol2
    else:
        phi = 0
        if eq(R[2][0], -1):
            th = pi / 2
            psi = phi + atan2(R[0][1], R[0][2])
        else:
            th = -pi / 2
            psi = -phi + atan2(-R[0][1], -R[0][2])
        return psi, th, phi


def get_angles_from_direction(direction: Vector):
    psi = 0
    if not eq(abs(direction[2]), 1):
        th1 = -asin(direction[2])
        th2 = pi - th1
        phi1 = atan2(direction[1] / cos(th1), direction[0] / cos(th1))
        phi2 = atan2(direction[1] / cos(th2), direction[0] / cos(th2))

        sol1 = (psi, th1, phi1)
        sol2 = (psi, th2, phi2)
        return sol1 if sum(map(abs, sol1)) < sum(map(abs, sol2)) else sol2
    else:
        phi = 0
        th = pi / 2 if eq(direction[2], -1) else -pi / 2
        return psi, th, phi


def degrees_tuple(radians):
    return tuple(map(degrees, radians))


def get_angles_deg_XZY(R):
    return degrees_tuple(get_angles_XZY(R))


def get_angles_deg_XYZ(R):
    return degrees_tuple(get_angles_XYZ(R))


def get_angles_XYZ(R):
    if (R[0][2] < 1):
        if (R[0][2] > -1):
            thetaY = asin(R[0][2])
            thetaX = atan2(-R[1][2], R[2][2])
            thetaZ = atan2(-R[0][1], R[0][0])
        else:
            thetaY = -pi / 2
            thetaX = -atan2(R[1][0], R[1][1])
            thetaZ = 0
        return thetaX, thetaY, thetaZ
    else:
        thetaY = pi / 2
        thetaX = atan2(R[1][0], R[1][1])
        thetaZ = 0
    return thetaX, thetaY, thetaZ


def get_angles_XZY(R):
    if (R[0][1] < 1):
        if (R[0][1] > -1):
            thetaZ = -asin(R[0][1])
            thetaX = atan2(R[2][1], R[1][1])
            thetaY = atan2(R[0][2], R[0][0])
        else:
            thetaZ = pi / 2
            thetaX = -atan2(R[2][0], R[2][2])
            thetaY = 0
        return thetaX, thetaY, thetaZ
    else:
        thetaZ = -pi / 2
        thetaX = atan2(-R[2][0], R[2][2])
        thetaY = 0
    return thetaX, thetaY, thetaZ


if __name__ == "__main__":
    a = get_matrix_XYZ(radians(0), radians(95.0), radians(0))
    angles = get_angles(a)
    print(*map(degrees, angles))
