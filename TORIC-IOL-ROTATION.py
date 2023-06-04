import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

def to_corneal_plane (vertex, spectacle_refraction):
    d = vertex/1000
    cp = spectacle_refraction / 1 -(d*spectacle_refraction)
    return cp

def to_spectacle_plane (vertex, corneal_plane_refraction):
    d = vertex/1000
    sp = corneal_plane_refraction / 1 +(d*corneal_plane_refraction)
    return sp


d = 12/1000



#cilinder at corneal plane
#current IOL axis
#current sphere
#current cylinder



def polar_to_rectangular(cylinder, axis):
    X = cylinder * math.cos(2*axis)
    Y = cylinder * math.sin(2 * axis)

    return (X, Y)




def astigmatism_correction(cil_cp, iol_ax, res_esf, res_cil, res_ax):
    res_esf = to_corneal_plane(d,res_esf)
    res_cil = to_corneal_plane(d, res_cil)
    if res_cil < 0:
        res_esf = res_esf + res_cil
        res_cil = - res_cil
        if res_ax <= 90:
            res_ax = res_ax + 90
        else:
            res_ax = res_ax - 90

    Ref_X, Ref_Y = polar_to_rectangular(res_cil,math.radians(res_ax))
    LT_X, LT_Y = polar_to_rectangular(cil_cp, math.radians(iol_ax))


    Astig_X = Ref_X + LT_X
    Astig_Y = Ref_Y + LT_Y
    angle = math.atan(Astig_Y/Astig_X)

    Astig = Astig_Y / math.sin(angle)

    # print(Astig)
    # print(math.degrees(angle)/2)

    degree_list = []

    for i in range(0,180):
        degree_list.append(i)

    # print(degree_list)

    rot_list = []
    rot_degree_list=[]

    for i in degree_list:
        LT_X, LT_Y = polar_to_rectangular(cil_cp, math.radians(i))
        Rot_X = Astig_X - LT_X
        Rot_Y = Astig_Y - LT_Y
        Rot_axis = math.atan(Rot_Y/Rot_X)
        Rot = Rot_Y / math.sin(Rot_axis)
        # print(Rot)
        if Rot_axis <0:
            Rot_axis = Rot_axis + math.pi

        Rot = Rot_Y / math.sin(Rot_axis)
         # print(Rot)
        rot_list.append(Rot)
        rot_degree_list.append(math.degrees(Rot_axis)/2)



    df_rango = pd.DataFrame((list(
            zip(rot_list, rot_degree_list))))
    df_rango.to_excel("refraction.xlsx")

    rot_list_abs = []
    for i in rot_list:
        i = math.sqrt(i*i)
        rot_list_abs.append(i)
    min_abs = min(rot_list_abs)

    index_min = rot_list_abs.index(min_abs)
    min_cil = rot_list[index_min]
    degree = degree_list[index_min]
    rot_degree = rot_degree_list[index_min]

    spherical_equivalent = res_esf + 0.5 * res_cil
    sphere = spherical_equivalent - 0.5 * (min_cil)
    if min_cil < 0:
        sphere = sphere + min_cil
        min_cil = - min_cil
        if rot_degree <= 90:
            rot_degree2 = rot_degree + 90
        else:
            rot_degree2 = rot_degree - 90
        rot_degree= rot_degree2
    sphere = to_spectacle_plane(d,sphere)
    min_cil = to_spectacle_plane(d, min_cil)
    rot_degree = round(rot_degree)
    res_esf_postrot =round(sphere,2)
    res_cil_postrot = round(min_cil, 2)
    res_axis_postrot = rot_degree
    ideal_iol_position = degree
    plt.plot(degree_list, rot_list)
    plt.scatter(ideal_iol_position, res_cil_postrot)
    t = ["Best IOL position: {}".format(ideal_iol_position)]
    t2 = ["Residual cylinder: {}".format(res_cil_postrot)]
    t3 = ["Axis of residual cylinder: {}".format(rot_degree)]
    plt.text(ideal_iol_position-40, res_cil_postrot-1, t)
    plt.text(ideal_iol_position - 40, res_cil_postrot - 1.5, t2)
    plt.text(ideal_iol_position - 40, res_cil_postrot - 2, t3)
    plt.show()

    return ideal_iol_position, res_esf_postrot, res_cil_postrot, res_axis_postrot



def grades_to_refraction(cil_cp, iol_ax, res_esf, res_cil, res_ax, iol_rotated):
    res_esf = to_corneal_plane(d, res_esf)
    res_cil = to_corneal_plane(d, res_cil)
    if res_cil < 0:
        res_esf = res_esf + res_cil
        res_cil = - res_cil
        if res_ax <= 90:
            res_ax = res_ax + 90
        else:
            res_ax = res_ax - 90

    Ref_X, Ref_Y = polar_to_rectangular(res_cil, math.radians(res_ax))
    LT_X, LT_Y = polar_to_rectangular(cil_cp, math.radians(iol_ax))

    Astig_X = Ref_X + LT_X
    Astig_Y = Ref_Y + LT_Y
    angle = math.atan(Astig_Y / Astig_X)

    Astig = Astig_Y / math.sin(angle)

    # print(Astig)
    # print(math.degrees(angle)/2)


    degree_list2 =[]
    # print(degree_list)
    for i in range(0,180):
        degree_list2.append(i)
    rot_list2 = []
    rot_degree_list = []

    for i in degree_list2:
        LT_X, LT_Y = polar_to_rectangular(cil_cp, math.radians(i))
        Rot_X = Astig_X - LT_X
        Rot_Y = Astig_Y - LT_Y
        Rot_axis = math.atan(Rot_Y / Rot_X)
        Rot = Rot_Y / math.sin(Rot_axis)
        # print(Rot)

        if Rot <0:
            Rot = -Rot
            Rot_axis = Rot_axis + math.pi
        # if Rot_axis < 0:
        #     Rot_axis = Rot_axis + math.pi

        Rot = Rot_Y / math.sin(Rot_axis)
        # print(Rot)
        rot_list2.append(Rot)
        rot_degree_list.append(math.degrees(Rot_axis) / 2)

    # df_rango = pd.DataFrame((list(
    #     zip(rot_list2, degree_list2))))
    # df_rango.to_excel("refraction3.xlsx")
    degree_list = [iol_rotated]
    print(degree_list)

    rot_list = []
    rot_degree_list = []

    for i in degree_list:
        LT_X, LT_Y = polar_to_rectangular(cil_cp, math.radians(i))
        Rot_X = Astig_X - LT_X
        Rot_Y = Astig_Y - LT_Y
        Rot_axis = math.atan(Rot_Y / Rot_X)
        Rot = Rot_Y / math.sin(Rot_axis)
        # print(Rot)


        if Rot_axis < 0:
            Rot_axis = Rot_axis + math.pi

        Rot = Rot_Y / math.sin(Rot_axis)
        # print(Rot)
        rot_list.append(Rot)
        rot_degree_list.append(math.degrees(Rot_axis) / 2)

    df_rango = pd.DataFrame((list(
        zip(rot_list, rot_degree_list))))
    df_rango.to_excel("refraction.xlsx")

    rot_list_abs = []
    for i in rot_list:

        i = math.sqrt(i * i)
        rot_list_abs.append(i)
    min_abs = min(rot_list_abs)
    print(min_abs)
    index_min = rot_list_abs.index(min_abs)
    min_cil = rot_list[index_min]
    degree = degree_list[index_min]
    rot_degree = rot_degree_list[index_min]

    spherical_equivalent = res_esf + 0.5 * res_cil
    sphere = spherical_equivalent - 0.5 * (min_cil)
    if min_cil < 0:
        sphere = sphere + min_cil
        min_cil = - min_cil
        if rot_degree <= 90:
            rot_degree2 = rot_degree + 90
        else:
            rot_degree2 = rot_degree - 90
        rot_degree = rot_degree2
    sphere = to_spectacle_plane(d, sphere)
    min_cil = to_spectacle_plane(d, min_cil)
    rot_degree = round(rot_degree)
    res_esf_postrot = round(sphere, 2)
    res_cil_postrot = round(min_cil, 2)
    res_axis_postrot = rot_degree
    ideal_iol_position = degree
    return ideal_iol_position, res_esf_postrot, res_cil_postrot, res_axis_postrot



def astigmatism_correction_modified(cil_cp, iol_ax, res_esf, res_cil, res_ax):
    res_esf = to_corneal_plane(d,res_esf)
    res_cil = to_corneal_plane(d, res_cil)
    if res_cil < 0:
        res_esf = res_esf + res_cil
        res_cil = - res_cil
        if res_ax <= 90:
            res_ax = res_ax + 90
        else:
            res_ax = res_ax - 90

    Ref_X, Ref_Y = polar_to_rectangular(res_cil,math.radians(res_ax))
    LT_X, LT_Y = polar_to_rectangular(cil_cp, math.radians(iol_ax))


    Astig_X = Ref_X + LT_X
    Astig_Y = Ref_Y + LT_Y
    angle = math.atan(Astig_Y/Astig_X)

    Astig = Astig_Y / math.sin(angle)

    # print(Astig)
    # print(math.degrees(angle)/2)

    degree_list = []

    for i in range(0,180):
        degree_list.append(i)

    # print(degree_list)

    rot_list = []
    rot_degree_list=[]

    for i in degree_list:
        LT_X, LT_Y = polar_to_rectangular(cil_cp, math.radians(i))
        Rot_X = Astig_X - LT_X
        Rot_Y = Astig_Y - LT_Y
        Rot_axis = math.atan(Rot_Y/Rot_X)
        Rot = Rot_Y / math.sin(Rot_axis)
        # print(Rot)
        if Rot < 0:
            Rot = -Rot
            Rot_axis = Rot_axis + math.pi


        Rot = Rot_Y / math.sin(Rot_axis)
         # print(Rot)
        rot_list.append(Rot)
        rot_degree_list.append(math.degrees(Rot_axis)/2)



    df_rango = pd.DataFrame((list(
            zip(rot_list, rot_degree_list))))
    df_rango.to_excel("refraction.xlsx")

    rot_list_abs = []
    for i in rot_list:
        i = math.sqrt(i*i)
        rot_list_abs.append(i)
    min_abs = min(rot_list_abs)

    index_min = rot_list_abs.index(min_abs)
    min_cil = rot_list[index_min]
    degree = degree_list[index_min]
    rot_degree = rot_degree_list[index_min]

    spherical_equivalent = res_esf + 0.5 * res_cil
    sphere = spherical_equivalent - 0.5 * (min_cil)
    if min_cil < 0:
        sphere = sphere + min_cil
        min_cil = - min_cil
        if rot_degree<0:
            print("aquí hay uno")
            rot_degree2 = rot_degree + 360
        if rot_degree <= 90:
            rot_degree2 = rot_degree + 90
        else:
            rot_degree2 = rot_degree - 90
        rot_degree= rot_degree2
    sphere = to_spectacle_plane(d,sphere)
    min_cil = to_spectacle_plane(d, min_cil)
    rot_degree = round(rot_degree)
    res_esf_postrot =round(sphere,2)
    res_cil_postrot = round(min_cil, 2)
    res_axis_postrot = rot_degree
    ideal_iol_position = degree
    return ideal_iol_position, res_esf_postrot, res_cil_postrot, res_axis_postrot


import pandas as pd
df = pd.read_excel("astigmatism2.xlsx", engine = "openpyxl")
print(df)
ideal_iol_position_list = []; res_esf_postrot_list = []; res_cil_postrot_list = []; res_axis_postrot_list = []
p = 0

for i in df["CilCP"]:
    ideal_iol_position, res_esf_postrot, res_cil_postrot, res_axis_postrot = grades_to_refraction(i, iol_ax=df["IOL_Ax"][p],
                                                                                                     res_esf=df["res_esf"][p], res_cil= df["res_cil"][p],
                                                                                                     res_ax= df["res_axis"][p], iol_rotated= df["eje lio post rot"][p])
    ideal_iol_position_list.append(ideal_iol_position), res_esf_postrot_list.append(
         res_esf_postrot), res_cil_postrot_list.append(res_cil_postrot), res_axis_postrot_list.append(res_axis_postrot)
    df_ex = pd.DataFrame(
        (list(zip(ideal_iol_position_list, res_esf_postrot_list, res_cil_postrot_list, res_axis_postrot_list))))
    df_ex.to_excel("astigmatism_ex_modified.xlsx")

    p = p + 1