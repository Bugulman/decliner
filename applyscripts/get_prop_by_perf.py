import pickle
from datetime import datetime
from pathlib import Path
import os


def create_report_dir(path):
    path = Path(path)
    path = path.joinpath("reports")
    path.mkdir(parents=True, exist_ok=True)
    os.chdir(path)
    print(os.getcwd())


def save_to_pickle():
    dens_prev = {}
    dens = {}
    create_report_dir(get_project_folder())
    try:
        # Пытаемся загрузить существующие данные
        with open("data.pickle", "rb") as f:
            dens_prev = pickle.load(f)
    except FileNotFoundError:
        # Файл не существует, создаем пустой словарь
        dens_prev = {}
    except Exception as e:
        raise Exception(f"Ошибка при загрузке данных: {e}")

    try:
        # Добавляем новые данные
        dens_g = get_property_by_name(name="DENG")
        dens_o = get_property_by_name(name="DENO")
        dens["deng"] = dens_g.compute_statistics(type="mean")
        dens["deno"] = dens_o.compute_statistics(type="mean")
        diff_g = dens_prev["deng"] - dens["deng"] if dens_prev["deng"] > 0 else 0
        diff_o = dens_prev["deno"] - dens["deno"] if dens_prev["deng"] > 0 else 0
        print(diff_g, diff_o)
        # Сохраняем обновленные данные
        with open("data.pickle", "wb") as f:
            pickle.dump(dens, f)  # Исправлено: dump вместо load

    except Exception as e:
        raise Exception(f"Ошибка при сохранении данных: {e}")


def __init_script__():  # use special function for the graph creation
    create_graph(
        name="crit_v", type="well", default_value=0, export=True
    )  # create a graph with wells in the list
    create_graph(
        name="crit_rate", type="well", default_value=0, export=True
    )  # create a graph with wells in the list


def crit_v_tochigin(rho_liquid: float, rho_gas: float, sigma_liquid_gas: float):
    """
    Terner criterion,
    Critical velocity, m/sec
    rho_liquid - density of liquid, kg/m3
    rho_gas - density of gas( on bottom hole pressure), kg/m3
    sigma_liquid_gas - IFT in liquid-gas system, N/m
    """
    g = 9.81  # m/sec2
    sigma_liquid_gas = sigma_liquid_gas * 10 ** (-3)  # convert dyn/sm3 in N/m
    velocity = (
        3.3
        * (
            (sigma_liquid_gas * g * (rho_liquid**2))
            / ((rho_liquid - rho_gas) * (rho_gas**2))
        )
        ** 0.25
    )
    return velocity


def crit_rate(rho_gas_bhp, rho_gas_st, crit_v, diam_t):
    """
    Critical gas rate, m3/day
    """
    import math

    A = (math.pi * (diam_t * (10 ** (-3))) ** 2) / 4
    print(f"Filtration area,bottom hole: {A} m3")
    rate = rho_gas_bhp * crit_v * A / rho_gas_st
    # convert to m3/day
    rate = rate * 24 * 3600
    return rate


def min_rate_calc():
    deng_first = 324.4
    deno_frist = 566
    well_data = {
        "1A011": {"DENG": 263.711123163684, "DENO": 557.708091301645},
        "1A012": {"DENG": 267.494099899723, "DENO": 559.506319973134},
        "1A021": {"DENG": 292.189827520906, "DENO": 576.991425816828},
        "1A022": {"DENG": 265.423494296631, "DENO": 573.028362521874},
        "1A023": {"DENG": 246.103163768554, "DENO": 562.69528167769},
        "1A024": {"DENG": 276.5916807378, "DENO": 569.793351083988},
        "1A031": {"DENG": 308.003039870583, "DENO": 565.963395703956},
        "1A032": {"DENG": 304.005368365104, "DENO": 564.556240332578},
        "1A033": {"DENG": 288.871982968466, "DENO": 562.619157883507},
        "1A041": {"DENG": 288.658150185955, "DENO": 554.795567663575},
        "1A042": {"DENG": 262.894432544641, "DENO": 568.603933018808},
        "1A043": {"DENG": 291.678677673054, "DENO": 563.322170475236},
        "1A044": {"DENG": 281.854908725683, "DENO": 554.838252583579},
        "1A045": {"DENG": 290.325901158343, "DENO": 554.187268685575},
        "1A046": {"DENG": 295.788172698236, "DENO": 552.115617617385},
        "1A051": {"DENG": 286.451076950368, "DENO": 578.462582707486},
        "1A052": {"DENG": 288.229460025389, "DENO": 580.70937111801},
        "1A053": {"DENG": 281.690255281051, "DENO": 566.291228374473},
        "1A054": {"DENG": 300.814799371343, "DENO": 562.346965936372},
        "1A071": {"DENG": 250.273669874653, "DENO": 573.803392418559},
        "1A072": {"DENG": 290.869911606314, "DENO": 543.051347283121},
        "1A073": {"DENG": 247.284565730363, "DENO": 578.41713051098},
        "1A081": {"DENG": 316.923001906951, "DENO": 570.538999082993},
        "1A082": {"DENG": 287.845241368435, "DENO": 573.586766172454},
        "1A083": {"DENG": 296.643949675542, "DENO": 573.294927381975},
        "1A091": {"DENG": 267.923565315648, "DENO": 563.772440457013},
        "1A092": {"DENG": 300.305811453468, "DENO": 549.939015877562},
        "1A093": {"DENG": 272.060625526776, "DENO": 570.33785412147},
        "1A093_2": {"DENG": 301.795991248252, "DENO": 562.844733863337},
        "1A094": {"DENG": 273.364744780268, "DENO": 567.004650595933},
        "1A095": {"DENG": 319.876480610197, "DENO": 549.248021215411},
        "1A096": {"DENG": 292.344596069349, "DENO": 562.200602864285},
        "1A111": {"DENG": 348.159254223523, "DENO": 574},
        "1A121": {"DENG": 276.801792301702, "DENO": 575.990891699552},
        "1A122": {"DENG": 281.900643540766, "DENO": 574.081205062359},
        "1A123": {"DENG": 287.932192236925, "DENO": 570.38781188681},
        "1A124": {"DENG": 292.708351247758, "DENO": 566.394821859878},
        "1A131": {"DENG": 289.119883237004, "DENO": 569.311361514178},
        "1A132": {"DENG": 277.132095260021, "DENO": 560.274966493822},
        "1A133": {"DENG": 282.352012102874, "DENO": 575.339968888119},
        "1A134": {"DENG": 281.699145564608, "DENO": 572.93473668411},
        "1A141": {"DENG": 265.724524225246, "DENO": 560.893103471235},
        "1A142": {"DENG": 271.348794628762, "DENO": 556.29968595386},
        "1A143": {"DENG": 269.811436138147, "DENO": 565.894612620614},
        "1A144": {"DENG": 265.912898665733, "DENO": 564.215553382812},
        "1A145": {"DENG": 267.538815482523, "DENO": 560.595608433335},
        "1A146": {"DENG": 269.434690684801, "DENO": 565.635810097184},
        "1A151": {"DENG": 276.12498874529, "DENO": 550.379955707537},
        "1A152": {"DENG": 262.663432747611, "DENO": 558.885943632821},
        "1A153": {"DENG": 261.636550723195, "DENO": 560.475528454017},
        "1A161": {"DENG": 274.274353574499, "DENO": 581.304356141044},
        "1A162": {"DENG": 256.53214268532, "DENO": 593.608342750566},
        "1A163": {"DENG": 278.379703954596, "DENO": 590.297733478161},
        "1A164": {"DENG": 351.007606160648, "DENO": 637.116072330756},
        "1A165B": {"DENG": 321.886594649153, "DENO": 617.903868843417},
        "1A166": {"DENG": 280.501734499185, "DENO": 595.513382073679},
        "1A171": {"DENG": 289.614780665383, "DENO": 573.068622235614},
        "1A172": {"DENG": 291.99611190667, "DENO": 568.653157728707},
        "1A173": {"DENG": 293.580433841778, "DENO": 570.54581066995},
        "1A174": {"DENG": 294.02831081326, "DENO": 571.568446706228},
        "1A175": {"DENG": 292.869963109758, "DENO": 580.167830225853},
        "1A181": {"DENG": 301.320763363346, "DENO": 561.754952378715},
        "1A182": {"DENG": 284.349561835811, "DENO": 571.159674872326},
        "1A183": {"DENG": 271.865588304465, "DENO": 577.780379527659},
        "1A191": {"DENG": 293.531620767076, "DENO": 571.491433044279},
        "1A192": {"DENG": 320.925425656014, "DENO": 568.105096737335},
        "1A193": {"DENG": 299.001127918635, "DENO": 564.804353890211},
        "1A194": {"DENG": 294.417094883825, "DENO": 566.917377036123},
        "1A195": {"DENG": 297.605073352994, "DENO": 565.489206945984},
        "1A196": {"DENG": 305.471664963973, "DENO": 563.653145032133},
        "1A201": {"DENG": 266.678723287134, "DENO": 565.636392288219},
        "1A202": {"DENG": 264.562658770484, "DENO": 564.225567601968},
        "1A203": {"DENG": 269.369403961972, "DENO": 564.126898669532},
        "1A204": {"DENG": 269.992642330881, "DENO": 567.287599060587},
        "1A205": {"DENG": 330.507835183836, "DENO": 557.810282423737},
        "1A206": {"DENG": 363.088894937187, "DENO": 554.967660391371},
        "1A211": {"DENG": 333.095791475343, "DENO": 551.052889600245},
        "1A212": {"DENG": 271.056764482639, "DENO": 577.479005533364},
        "1A213": {"DENG": 254.860954958757, "DENO": 569.744825356251},
        "1A214": {"DENG": 296.774748421776, "DENO": 556.959122571414},
        "1A221": {"DENG": 274.653155229925, "DENO": 568.981832257977},
        "1A222": {"DENG": 294.921310100596, "DENO": 569.920245815857},
        "1A223": {"DENG": 279.728571521751, "DENO": 568.776088653059},
        "1A231": {"DENG": 305.191608414415, "DENO": 566.427282671339},
        "1A232": {"DENG": 279.624651479007, "DENO": 566.13659516569},
        "1A233": {"DENG": 285.292833111575, "DENO": 573.177552835934},
        "1A234": {"DENG": 321.132525306233, "DENO": 555.840078719371},
        "1A241": {"DENG": 286.149819491189, "DENO": 558.914388625302},
        "1A242": {"DENG": 262.346543424001, "DENO": 560.463809136793},
        "1A243": {"DENG": 304.630276764621, "DENO": 549.173037493655},
        "1A244": {"DENG": 295.435572123403, "DENO": 555.102520228243},
        "1A245": {"DENG": 290.072585522822, "DENO": 558.69968350438},
        "1A246": {"DENG": 280.036980492616, "DENO": 555.382723349129},
        "1A271": {"DENG": 327.536965742831, "DENO": 543.804089049217},
        "1A272": {"DENG": 328.772920664601, "DENO": 558.003969984263},
        "1A273": {"DENG": 337.168891732407, "DENO": 540.615951261226},
        "1A281": {"DENG": 292.98781225815, "DENO": 568.127626131824},
        "1A282": {"DENG": 300.91844253839, "DENO": 573.42265255166},
        "1A283": {"DENG": 305.144285331978, "DENO": 567.615113199694},
        "1A301": {"DENG": 314.220535637869, "DENO": 560.611375379098},
        "1A302": {"DENG": 321.754228927764, "DENO": 561.952850491362},
        "1A303": {"DENG": 274.774699864644, "DENO": 567.619625647213},
        "1A304": {"DENG": 286.408599137216, "DENO": 569.427239224026},
        "1A311": {"DENG": 291.17298997137, "DENO": 563.845931058271},
        "1A312": {"DENG": 323.748663240719, "DENO": 560.619491377229},
        "1A313": {"DENG": 338.994716520277, "DENO": 569.835966330963},
        "1A313G": {"DENG": 339.636286304893, "DENO": 572.405259536032},
        "1A313_2": {"DENG": 339.636286304893, "DENO": 572.405259536032},
        "1A313_OLD": {"DENG": 338.994716520277, "DENO": 569.835966330963},
        "1A314": {"DENG": 330.646344515042, "DENO": 567.454401331142},
        "1A321": {"DENG": 326.992192052656, "DENO": 541.522134864849},
        "1A322": {"DENG": 316.366552664115, "DENO": 537.124902356201},
        "1A323": {"DENG": 365.293412353108, "DENO": 518.096263382454},
        "1A324": {"DENG": 330.624048314979, "DENO": 543.256053691815},
        "1A331": {"DENG": 287.207372253861, "DENO": 567.140596795406},
        "1A332": {"DENG": 326.909107463554, "DENO": 540.579381675873},
        "1A333": {"DENG": 339.270728169854, "DENO": 530.993399907014},
        "1A013": {"DENG": 294.432930802346, "DENO": 546.806209932435},
        "1A184": {"DENG": 352.470669244115, "DENO": 564.149458159085},
        "1A341": {"DENG": 391.716055186451, "DENO": 566},
        "1A342": {"DENG": 351.761446060468, "DENO": 566.087480487798},
        "1A343": {"DENG": 373.211674510326, "DENO": 569.514080191042},
        "1A344": {"DENG": 342.777849777212, "DENO": 564.174254360349},
    }
    crit_v = get_global_graph(name="crit_v")
    crit_grate = get_global_graph(name="crit_rate")
    dens_g = get_property_by_name(name="DENG").compute_statistics(type="mean")
    dens_o = get_property_by_name(name="DENO").compute_statistics(type="mean")
    diff_g = deng_first - dens_g
    diff_o = deno_frist - dens_o
    for w in get_all_wells():
        w_dg = well_data[w.name]["DENG"] - diff_g
        w_do = well_data[w.name]["DENO"] - diff_o
        crit_v = crit_v_tochigin(w_do, w_dg, 20)
        crit_grate[w] = crit_rate(w_dg, wgdn[w], crit_v, 157)
        crit_v[w] = crit_v
    export(crit_v, name="crit_v")
    export(crit_grate, name="crit_rate")
