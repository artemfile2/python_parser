# -*- coding: utf-8 -*-

import datetime
import xml.etree.cElementTree as ET
from PyQt5 import QtWidgets

from myconverter import convert_none_type
from excel import export_xls

from connect import *
# from threading import Thread


def delete_from_db(month, year, glpu):
    """
    Удаление данных в таблицах по коду МО и периоду
    """
    try:
        db = con('db')
        dbcur = db.cursor()
        dbcur.execute("""CALL DELETE_DATA(:period, :date_per, :glpu)""",
                        (month + year, '01.' + month + '.' + year, glpu))
        db.commit()
        dbcur.close()
    except cx_Oracle.Error as err:
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Query error: {}".format(err))
        msg.setWindowTitle("Ошибка в запросе на удаление")
        msg.setDetailedText("Query error delete: {}".format(err))
        msg.exec_()
        print(err)


def xml_2_db(path, xml):
    """
        Парсинг XML файла и запись строк в базу
    """
    try:
        db = con('db')
        dbcur = db.cursor()

        tree = ET.parse(path + '\\' + xml)
        glpu_g = xml[12:18]
        if xml[0] == 'L':
            year = '20' + xml[8:10]
            month = xml[10:12]
            glpu_l = xml[12:18]

            element_xml_root = tree.getroot()
            try:
                query = dbcur.prepare('INSERT INTO XML_PACIENT PARTITION(p{})'
                                      '(id_pac, glpu, fam, im, ot, w, dr, dost, fam_p, im_p, ot_p, dr_p, dost_p, w_p,'
                                      'mr, doctype, docser, docnum, snils, adres, ident_sp, polis, novor, inv, mse,'
                                      'period) '
                                      'VALUES (:id_pac, :glpu_l, :fam, :im, :ot, :w, :dr, :dost, :fam_p, :im_p, :ot_p,'
                                      ':dr_p, :dost_p, :w_p, :mr, :doctype, :docser, :docnum, :snils, :adres, :ident_sp,'
                                      ':id_pac, :novor, :inv, :mse, :period)'.format(month + year))

                for elem_pers in element_xml_root.findall('PERS'):
                    id_pac = convert_none_type(elem_pers.find('ID_PAC'))
                    fam = convert_none_type(elem_pers.find('FAM'))
                    im = convert_none_type(elem_pers.find('IM'))
                    ot = convert_none_type(elem_pers.find('OT'))
                    w = convert_none_type(elem_pers.find('W'))
                    dr = convert_none_type(elem_pers.find('DR'))
                    dost = convert_none_type(elem_pers.find('DOST'))
                    fam_p = convert_none_type(elem_pers.find('FAM_P'))
                    im_p = convert_none_type(elem_pers.find('IM_P'))
                    ot_p = convert_none_type(elem_pers.find('OT_P'))
                    dr_p = convert_none_type(elem_pers.find('DR_P'))
                    dost_p = convert_none_type(elem_pers.find('DOST_P'))
                    w_p = convert_none_type(elem_pers.find('W_P'))
                    mr = convert_none_type(elem_pers.find('MR'))
                    doctype = elem_pers.find('DOCTYPE').text
                    docser = elem_pers.find('DOCSER').text
                    docnum = elem_pers.find('DOCNUM').text
                    snils = convert_none_type(elem_pers.find('SNILS'))
                    # okatog = elem_pers.find('OKATOG').text
                    # okatop = elem_pers.find('OKATOP').text
                    adres = convert_none_type(elem_pers.find('ADRES'))
                    ident_sp = convert_none_type(elem_pers.find('IDENT_SP'))
                    # comentp = elem_pers.find('COMENTP').text
                    # vpolis = elem_pers.find('VPOLIS').text
                    novor = convert_none_type(elem_pers.find('NOVOR'))
                    inv = convert_none_type(elem_pers.find('INV'))
                    mse = convert_none_type(elem_pers.find('MSE'))

                    if w == '':
                        w = 0

                    if dr == '':
                        dr1 = datetime.strptime('1900-01-01', "%Y-%m-%d")
                    else:
                        dr1 = datetime.strptime(dr, "%Y-%m-%d")

                    if dr_p == '':
                        dr2_p = datetime.strptime('1900-01-01', "%Y-%m-%d")
                    else:
                        dr2_p = datetime.strptime(dr_p, "%Y-%m-%d")

                    dbcur.execute(query, (id_pac, glpu_l, fam, im, ot, w, dr1, dost, fam_p, im_p, ot_p, dr2_p,
                                          dost_p, w_p, mr, doctype, docser, docnum, snils, adres, ident_sp, id_pac,
                                          novor, inv, mse, datetime.strptime('01.'+month+'.'+year, "%d.%m.%Y")))
            except cx_Oracle.Error as err:
                print(f'Query error при добавлении в XML_PACIENT: {err}')

        if xml[0] == 'H':
            year = '20'+xml[8:10]
            month = xml[10:12]
            glpu = xml[12:18]

            element_xml_root = tree.getroot()
            for element in element_xml_root.findall('ZAP'):
                for pac in element.findall('PACIENT'):
                    try:
                        idpac = convert_none_type(pac.find('ID_PAC'))
                        vpolis = convert_none_type(pac.find('VPOLIS'))
                        spolis = convert_none_type(pac.find('SPOLIS'))
                        npolis = convert_none_type(pac.find('NPOLIS'))
                        # stokato = convert_none_type(pac.find('ST_OKATO'))
                        smo = convert_none_type(pac.find('SMO'))
                        smoogrn = convert_none_type(pac.find('SMO_OGRN'))
                        smook = convert_none_type(pac.find('SMO_OK'))
                        smonam = convert_none_type(pac.find('SMO_NAM'))
                        novor = convert_none_type(pac.find('NOVOR'))
                        vnov_d = convert_none_type(pac.find('VNOV_D'))

                        queryPT2 = dbcur.prepare('INSERT INTO XML_PACIENT_EXT PARTITION(p{}) '
                                                 '(id_pac, vpolis, spolis, npolis, smo, smo_ogrn, smo_ok, smo_nam,'
                                                 ' novor, vnov_d, glpu, period)'
                                                 ' VALUES '
                                                 '(:idpac, :vpolis, :spolis, :npolis, :smo, :smo_ogrn, :smo_ok, '
                                                 ' :smo_nam, :novor, :vnov_d, :glpu, :period)'.format(month + year))

                        dbcur.execute(queryPT2, (idpac, vpolis, spolis, npolis, smo, smoogrn, smook,
                                                smonam, novor, vnov_d, glpu,
                                                datetime.strptime('01.' + month + '.' + year, "%d.%m.%Y")))
                    except cx_Oracle.Error as err:
                        print(f'Query error при UPDATE в XML_PACIENT: {err}')

                for slu in element.findall('SLUCH'):
                    idcase = slu.find('IDCASE').text
                    usl_ok = slu.find('USL_OK').text
                    vidpom = slu.find('VIDPOM').text
                    for_pom = slu.find('FOR_POM').text
                    disp = slu.find('DISP').text
                    vid_hmp = convert_none_type(slu.find('VID_HMP'))
                    metod_hmp = convert_none_type(slu.find('METOD_HMP'))
                    npr_mo = convert_none_type(slu.find('NPR_MO'))
                    extr = slu.find('EXTR').text
                    lpu = slu.find('LPU').text
                    lpu_1 = slu.find('LPU_1').text
                    podr = slu.find('PODR').text
                    profil = slu.find('PROFIL').text
                    det = slu.find('DET').text
                    nhistory = slu.find('NHISTORY').text
                    date_1 = slu.find('DATE_1').text
                    date_2 = slu.find('DATE_2').text
                    ds0 = slu.find('DS0').text
                    ds1 = slu.find('DS1').text
                    ds2 = slu.find('DS2').text
                    ds3 = convert_none_type(slu.find('DS3'))
                    vnov_m = convert_none_type(slu.find('VNOV_M'))
                    code_mes1 = slu.find('CODE_MES1').text
                    code_mes2 = slu.find('CODE_MES2').text
                    rslt = slu.find('RSLT').text
                    rslt_d = convert_none_type(slu.find('RSLT_D'))
                    ishod = slu.find('ISHOD').text
                    prvs = slu.find('PRVS').text
                    vers_spec = slu.find('VERS_SPEC').text
                    iddokt = convert_none_type(slu.find('IDDOKT'))
                    os_sluch = slu.find('OS_SLUCH').text
                    idsp = slu.find('IDSP').text
                    ed_col = 0 if \
                                   convert_none_type(slu.find('ED_COL')) == '' \
                               else \
                                   float(convert_none_type(slu.find('ED_COL')))
                    tarif = float(slu.find('TARIF').text)
                    sumv = float(slu.find('SUMV').text)
                    oplata = slu.find('OPLATA').text
                    sump = float(slu.find('SUMP').text)
                    # sank_it = float(slu.find('SANK_IT').text)
                    tal_d = convert_none_type(slu.find('TAL_D'))
                    tal_p = convert_none_type(slu.find('TAL_P'))
                    vbr = convert_none_type(slu.find('VBR'))
                    p_otk = convert_none_type(slu.find('P_OTK'))
                    nrisoms = slu.find('NRISOMS').text
                    ds1_pr = slu.find('DS1_PR').text
                    ds4 = slu.find('DS4').text

                    if convert_none_type(slu.find('NAZN')) == '':
                        nazn = convert_none_type(slu.find('NAZR'))
                    elif convert_none_type(slu.find('NAZR')) == '':
                        nazn = convert_none_type(slu.find('NAZN'))
                    else:
                        nazn = convert_none_type(slu.find('NAZN'))

                    naz_sp = slu.find('NAZ_SP').text
                    naz_v = slu.find('NAZ_V').text
                    naz_pmp = slu.find('NAZ_PMP').text
                    naz_pk = slu.find('NAZ_PK').text
                    pr_d_n = slu.find('PR_D_N').text
                    comentsl = slu.find('COMENTSL').text
                    pr_nov = slu.find('PR_NOV').text
                    novor_sl = slu.find('NOVOR').text
                    orders = slu.find('ORDER').text
                    t_order = slu.find('T_ORDER').text
                    kem_prov = slu.find('KEM_PROV').text
                    stat = convert_none_type(slu.find('STAT'))
                    smo_sl = slu.find('SMO').text
                    nprdate = convert_none_type(slu.find('NPR_DATE'))
                    talnum = convert_none_type(slu.find('TAL_NUM'))

                    try:
                        queryTT = dbcur.prepare('INSERT INTO XML_SLUCH PARTITION(sl{}) (glpu, mcod, idcase, usl_ok, '
                                    'vidpom, for_pom, disp, vid_hmp, metod_hmp, npr_mo, extr, podr, profil, det, '
                                    'nhistory, date_1, date_2, ds0, ds1, ds2, ds3, vnov_m, code_mes1, code_mes2, '
                                    'rslt, rslt_d, ishod, prvs_s, vers_spec, iddokt, os_sluch, idsp, ed_col, tarif, '
                                    'sumv, oplata, sump, tal_d, tal_p, vbr, p_otk, nrisoms, ds1_pr, ds4, nazn, naz_sp, '
                                    'naz_v, naz_pmp, naz_pk, pr_d_n, comentsl, pr_nov, novor, order_, t_order, '
                                    'kem_prov, smo, id_sluch_tt, prizn_prov, id_pac, stat, npr_date, tal_num, period) '
                                    'VALUES (:lpu, :lpu_1, :idcase, :usl_ok, :vidpom, :for_pom, :disp, '
                                    ':vid_hmp, :metod_hmp, :npr_mo, :extr, :podr, :profil, :det, :nhistory, '
                                    ':dt1, :dt2, :ds0, :ds1, :ds2, :ds3, :vnov_m, :code_mes1, :code_mes2, '
                                    ':rslt, :rslt_d, :ishod, :prvs, :vers_spec, :iddokt, :os_sluch, :idsp, '
                                    ':ed_col, :tarif, :sumv, :oplata, :sump, :dtd, :dtp, :vbr, :p_otk, '
                                    ':nrisoms, :ds1_pr, :ds4, :nazn, :naz_sp, :naz_v, :naz_pmp, :naz_pk, '
                                    ':pr_d_n, :comentsl, :pr_nov, :novor_sl, :orders, :t_order, :kem_prov, '
                                    ':smo_sl, :ids, :prizn_prov, :idpac, :stat, :nprdat, :talnum, :period)'.format(
                                                                                                          month + year
                                                                                                          )
                                    )

                        dt1 = datetime.strptime(date_1, "%Y-%m-%d")
                        dt2 = datetime.strptime(date_2, "%Y-%m-%d")

                        if nprdate == '':
                            nprdat = datetime.strptime('1900-01-01', "%Y-%m-%d")
                        else:
                            nprdat = datetime.strptime(nprdate, "%Y-%m-%dT%H:%M:%S").date()

                        if tal_d == '':
                            dtd = datetime.strptime('1900-01-01', "%Y-%m-%d")
                        else:
                            dtd = datetime.strptime(tal_d, "%Y-%m-%d")

                        if tal_p == '':
                            dtp = datetime.strptime('1900-01-01', "%Y-%m-%d")
                        else:
                            dtp = datetime.strptime(tal_p, "%Y-%m-%d")

                        dbcur.execute(queryTT, (lpu, lpu_1, idcase, usl_ok, vidpom, for_pom, disp, vid_hmp,
                                    metod_hmp, npr_mo, extr, podr, profil, det, nhistory, dt1, dt2, ds0,
                                    ds1, ds2, ds3, vnov_m, code_mes1, code_mes2, rslt, rslt_d, ishod, prvs,
                                    vers_spec, iddokt, os_sluch, idsp, ed_col, tarif, sumv, oplata, sump,
                                    dtd, dtp, vbr, p_otk, nrisoms, ds1_pr, ds4, nazn, naz_sp, naz_v, naz_pmp,
                                    naz_pk, pr_d_n, comentsl, pr_nov, novor_sl, orders, t_order, kem_prov, smo_sl,
                                    idcase, 0, idpac, stat, nprdat, talnum,
                                    datetime.strptime('01.'+month+'.'+year, "%d.%m.%Y")))
                    except cx_Oracle.Error as err:
                        print(f'Query error при добавлении в XML_SLUCH: {err} lpu-{lpu} idcase-{idcase}')

                    for usl in slu.findall('USL'):
                        idserv = usl.find('IDSERV').text
                        lpu_u = usl.find('LPU').text
                        lpu_1u = usl.find('LPU_1').text
                        podr = convert_none_type(usl.find('PODR'))
                        profil_u = usl.find('PROFIL').text
                        det = usl.find('DET').text
                        date_in = usl.find('DATE_IN').text
                        date_out = usl.find('DATE_OUT').text
                        ds = usl.find('DS').text
                        code_usl = convert_none_type(usl.find('CODE_USL'))
                        ed_col_u = 0 if \
                                        convert_none_type(usl.find('ED_COL')) == '' \
                                    else \
                                        float(convert_none_type(usl.find('ED_COL')))
                        koef_k = 0 if \
                                      convert_none_type(usl.find('KOEF_K')) == '' \
                                  else \
                                      float(convert_none_type(usl.find('KOEF_K')))
                        pouh = usl.find('POUH').text
                        zak = convert_none_type(usl.find('ZAK'))
                        kol_usl = float(usl.find('KOL_USL').text)
                        tarif = float(usl.find('TARIF').text)
                        sumv_usl = float(usl.find('SUMV_USL').text)
                        prvs = convert_none_type(usl.find('PRVS'))
                        code_md = usl.find('CODE_MD').text
                        comentu = convert_none_type(usl.find('COMENTU'))
                        dir2 = usl.find('DIR2').text
                        gr_zdorov = usl.find('GR_ZDOROV').text
                        student = usl.find('STUDENT').text
                        spolis_u = convert_none_type(usl.find('SPOLIS'))
                        npolis_u = convert_none_type(usl.find('NPOLIS'))
                        stat_u = convert_none_type(usl.find('STAT'))
                        stand = usl.find('STAND').text
                        p_per = usl.find('P_PER').text
                        npl = usl.find('NPL').text
                        idsh = convert_none_type(usl.find('idsh'))

                        try:
                            query_u = dbcur.prepare('INSERT INTO XML_USL PARTITION(u{}) (lpu, lpu_1, ID_SLUCH, idserv, '
                                                  'podr, profil, det, date_in, date_out, ds, code_usl, ed_col, koefk, '
                                                  'pouh, zak, kol_usl, tarif, sumv_usl, sumv_oms, prvs_u, code_md,'
                                                  'comentu, dir2, gr_zdorov, student, spolis, npolis, stand, p_per, '
                                                  'npl, idsh, id_pac, stat, period) '
                                                  ' VALUES (:lpu_u, :lpu_1u, :idcase, :idserv, :podr, :profil_u, :det, '
                                                  ':date_in, :date_out, :ds, :code_usl, :ed_col_u, :koef_k, :pouh, :zak, '
                                                  ':kol_usl, :tarif, :sumv_usl, :sumv_usl, :prvs, :code_md, :comentu, '
                                                  ':dir2, :gr_zdorov, :student, :spolis_u, :npolis_u, :stand, :p_per, '
                                                  ':npl, :idsh, :idpac, :stat_u, :period)'.format(month + year))

                            dtin = datetime.strptime(date_in, "%Y-%m-%d")
                            dtout = datetime.strptime(date_out, "%Y-%m-%d")

                            dbcur.execute(query_u, (lpu_u, lpu_1u, idcase, idserv, podr, profil_u, det, dtin, dtout,
                                                  ds, code_usl, ed_col_u, koef_k, pouh, zak, kol_usl, tarif,
                                                  sumv_usl, sumv_usl, prvs, code_md, comentu, dir2, gr_zdorov, student,
                                                  spolis_u, npolis_u, stand, p_per, npl, idsh, idpac, stat_u,
                                                  datetime.strptime('01.' + month + '.' + year, "%d.%m.%Y")))

                        except cx_Oracle.Error as err:
                            print(f'Query error при добавлении в XML_USL: {err} lpu-{lpu_u} idserv-{idserv}')


                        for napr in usl.findall('NAPR'):
                            try:
                                napr_date = napr.find('NAPR_DATE').text
                                napr_v = napr.find('NAPR_V').text
                                met_issl = napr.find('MET_ISSL').text
                                napr_usl = napr.find('NAPR_USL').text

                                query_napr = dbcur.prepare('INSERT INTO XML_NAPR (idserv, glpu, period, napr_date, '
                                                           'napr_v, met_issl, napr_usl) '
                                                           'VALUES (:idserv, :glpu, :period, :napr_date, :napr_v, '
                                                           ':met_issl, :napr_usl)')

                                dbcur.execute(query_napr, (idserv, lpu_u, '01.' + month + '.' + year), napr_date,
                                              napr_v, met_issl, napr_usl)

                            except:
                                print('Query error при добавлении в XML_NAPR')

                        for onk_usl in usl.findall('ONK_USL'):
                            try:
                                id_onk = onk_usl.find('ID').text
                                ds1_t = onk_usl.find('DS1_T').text
                                stad = onk_usl.find('STAD').text
                                onk_t = onk_usl.find('ONK_T').text
                                onk_n = onk_usl.find('ONK_N').text
                                onk_m = onk_usl.find('ONK_M').text
                                mtstz = onk_usl.find('MTSTZ').text
                                sod = float(onk_usl.find('SOD').text)
                                pr_cons = onk_usl.find('PR_CONS').text
                                usl_tip = onk_usl.find('USL_TIP').text
                                hir_tip = onk_usl.find('HIR_TIP').text
                                lek_tip_l = onk_usl.find('LEK_TIP_L').text
                                lek_tip_v = onk_usl.find('LEK_TIP_V').text
                                luch_tip = onk_usl.find('LUCH_TIP').text
                                dt_cons = onk_usl.find('DT_CONS').text

                                query_onk = dbcur.prepare('INSERT INTO XML_ONK (idserv, id, glpu, period, ds1_t, '
                                                           'stad, onk_t, onk_n, onk_m, mtstz, sod, pr_cons, usl_tip,'
                                                           'hir_tip, lek_tip_l, lek_tip_v, luch_tip, dt_cons) '
                                                           'VALUES (:idserv, :id, :glpu, :period, :ds1_t, :stad, '
                                                           ':onk_t, :onk_n, :onk_m, :mtstz, :sod, :pr_cons, :usl_tip,'
                                                           ':hir_tip, :lek_tip_l, :lek_tip_v, :luch_tip, :dt_cons)')

                                dtonk = datetime.strptime(dt_cons, "%Y-%m-%dT%H:%M:%S").date()
                                dbcur.execute(query_onk, (idserv, id_onk, lpu_u, '01.' + month + '.' + year,
                                                          ds1_t, stad, onk_t, onk_n, onk_m, mtstz, sod, pr_cons,
                                                          usl_tip, hir_tip, lek_tip_l, lek_tip_v, luch_tip, dtonk))

                            except:
                                print('Query error при добавлении в XML_ONK')

                            for diag in onk_usl.findall('B_DIAG'):
                                try:
                                    diag_tip = diag.find('DIAG_TIP').text
                                    diag_code = diag.find('DIAG_CODE').text
                                    diag_rslt = diag.find('DIAG_RSLT').text

                                    query_diag = dbcur.prepare('INSERT INTO XML_DIAG (idserv, id, glpu, period,'
                                                               'diag_tip, diag_code, diag_rslt) '
                                                               'VALUES (:idserv, :id, :glpu, :period, :diag_tip, '
                                                               ':diag_code, :diag_rslt)')

                                    dbcur.execute(query_diag, (idserv, id_onk, lpu_u, '01.' + month + '.' + year,
                                                               diag_tip, diag_code, diag_rslt))

                                except:
                                    print('Query error при добавлении в XML_DIAG')

                            for bprot in onk_usl.findall('B_PROT'):
                                try:
                                    prot = convert_none_type(bprot.find('PROT'))
                                    d_prot = convert_none_type(bprot.find('D_PROT'))

                                    query_prot = dbcur.prepare('INSERT INTO XML_PROT (idserv, id, glpu, period,'
                                                               'prot, d_prot) '
                                                               'VALUES (:idserv, :id, :glpu, :period, '
                                                               ':prot, :d_prot)')

                                    dbcur.execute(query_prot, (idserv, id_onk, lpu_u, '01.' + month + '.' + year,
                                                               prot, d_prot))

                                except:
                                    print('Query error при добавлении в XML_PROT')

                        for vmp_oper in usl.findall('HRRGD'):
                            if convert_none_type(vmp_oper.find('HKOD')) == '':
                                vid_vme = convert_none_type(vmp_oper.find('VID_VME'))
                            elif convert_none_type(vmp_oper.find('VID_VME')) == '':
                                vid_vme = convert_none_type(vmp_oper.find('HKOD'))
                            else:
                                vid_vme = 'error'

                            ksgh = convert_none_type(vmp_oper.find('KSGH'))
                            idnomk = convert_none_type(vmp_oper.find('IDNOMK'))
                            name_o = vmp_oper.find('NAME_O').text

                            try:
                                query_oper = dbcur.prepare('INSERT INTO XML_HRRGD (glpu, mcod, idserv, hkod, ksgh,'
                                                           'idnomk, name_o, period) '
                                                           'VALUES (:glpu, :mcod, :idserv, :hkod, :ksgh, :idnomk, '
                                                           ':name_o, :period)')

                                dbcur.execute(query_oper, (lpu, lpu_1, idserv, vid_vme, ksgh, idnomk, name_o,
                                                      '01.' + month + '.' + year))

                            except cx_Oracle.Error as err:
                                print(f'Query error при добавлении в XML_HRRGD: {err}')

            for element_doc in element_xml_root.findall('VRACH'):
                try:
                    kod = convert_none_type(element_doc.find('KOD'))
                    fio = convert_none_type(element_doc.find('FIO'))
                    mcod = convert_none_type(element_doc.find('LPU_1'))
                    idmsp = convert_none_type(element_doc.find('IDMSP'))
                    spec = convert_none_type(element_doc.find('SPEC'))
                    if kod:
                        queryDT = dbcur.prepare('INSERT INTO XML_VRACH (glpu, mcod, kod, fio, idmsp, spec, period) '
                                                'VALUES (:glpu, :mcod, :kod, :fio, :idmsp, :spec, :period)')
                        dbcur.execute(queryDT, (glpu, mcod, kod, fio, idmsp, spec,
                                                '01.' + month + '.' + year))
                except cx_Oracle.Error as err:
                    print(f'Query error при добавлении в XML_VRACH {err}')

            for element_shet in element_xml_root.findall('SCHET'):
                code = element_shet.find('CODE').text
                code_mo = element_shet.find('CODE_MO').text
                year_s = element_shet.find('YEAR').text
                month_s = element_shet.find('MONTH').text
                nschet = element_shet.find('NSCHET').text
                dschet = element_shet.find('DSCHET').text
                plat = element_shet.find('PLAT').text
                summav = float(element_shet.find('SUMMAV').text)
                coments = element_shet.find('COMENTS').text
                summap = float(element_shet.find('SUMMAP').text)

                try:
                    queryST = dbcur.prepare('INSERT INTO XML_SCHET (code, glpu, yer, mont, nschet, dschet, plat, '
                                            'summav, coments, summap, period) '
                                            'VALUES (:code, :glpu, :year_s, :month_s, :nschet, :dt, :plat, '
                                            ':summav, :coments, :summap, :period)')

                    dt = datetime.strptime(dschet, "%Y-%m-%dT%H:%M:%S").date()
                    dbcur.execute(queryST, (code, code_mo, year_s, month_s, nschet, dt, plat, summav, coments, summap,
                                            '01.' + month + '.' + year))

                except cx_Oracle.Error as err:
                    print(f'Query error при добавлении в XML_SCHET: {err}')

            try:
                queryF = dbcur.prepare('INSERT INTO all_files (date_in, glpu, priz, year, month, date_out) '
                                       'VALUES (:dt, :glpu, :priz, :year, :month, SYSDATE)')

                dt = os.path.getmtime(path + '\\' + xml)
                dt = datetime.fromtimestamp(dt)
                dbcur.execute(queryF, (dt, glpu, xml[18:19], year, month))

            except cx_Oracle.Error as err:
                print(f'Query error при добавлении в all_files: {err}')

        db.commit()

        os.remove(path + '\\' + xml)

        try:
            if xml[0] == 'H':
                query_RUN = "CALL RUN_EXP_PROC(:period, :period_date, :glpu)"
                dbcur.execute(query_RUN, (month + year, '01.' + month +'.'+ year, glpu_g))

                dbcur.close()

                export_xls('01.' + month + '.' + year, glpu_g)
        except cx_Oracle.Error as err:
            print(f'Query error при вызове RUN_EXP_PROC: {err}')

    except IOError as err:
        print(err)


def get_file_xml(xml_file, year, month, glpu):
    """
    Функция получения наименования XML файлов из zip архива
    если данные по коду есть в базе, удаляются все данные по данному периоду и коду МО
    """
    try:
        pathxml = os.path.dirname(xml_file)
        typefile = os.path.basename(xml_file)[-5]
        files = os.listdir(pathxml)
        xml = list(filter(lambda x: x.endswith(year[2:4] + month + glpu + typefile + '.XML'), files))

        delete_from_db(month, year, glpu)

        xml.reverse()
        for file in xml:
            xml_2_db(pathxml, file)

    except IOError as err:
        print(err)