from connect import *
import os
import xml.etree.ElementTree as ET


"""
    функция проверки поля в XML
    если поля нет или NUll то 
    чтобы ошибки не было возвращаю пустую строку 
"""
def convert_none_type(obj):
    try:
        if obj is None:
            return ''
        else:
            if obj.text is None:
                return ''
            else:
                return obj.text
    except TypeError:
        return ''


def DeleteFromDB(glpu):
    try:
        db = con('db')
        dbcur = db.cursor()

        queryPTs = """DELETE FROM PT05S502018051_COPY WHERE glpu = {!r}""".format(glpu)
        dbcur.execute(queryPTs)
        queryTTs = """DELETE FROM TT05S50201805_COPY WHERE glpu = {!r}""".format(glpu)
        dbcur.execute(queryTTs)
        queryDTs = """DELETE FROM DT05S50201805_COPY WHERE glpu = {!r}""".format(glpu)
        dbcur.execute(queryDTs)
        querySTs = """DELETE FROM ST05S50201805_COPY WHERE glpu = {!r}""".format(glpu)
        dbcur.execute(querySTs)
        queryUTs = """DELETE FROM UT05S50201805_COPY WHERE lpu = {!r}""".format(glpu)
        dbcur.execute(queryUTs)
        queryNTs = """DELETE FROM NT05S50201805_COPY WHERE glpu = {!r}""".format(glpu)
        dbcur.execute(queryNTs)

        # print(f'Удаление данных МО {glpu} из таблиц завершенно!')
        db.commit()
        dbcur.close()

    except IOError as err:
        print(err)


"""
Парсинг XML файла и запись строк в базу
"""
def XmlToDB(path, xml):
    try:
        tree = ET.parse(path + '\\' + xml)
        if xml[0] == 'H':
            year = '20'+xml[8:10]
            month = xml[10:12]
            glpu = xml[12:18]

            db = con('db')
            dbcur = db.cursor()
            element_xml_root = tree.getroot()
            for element in element_xml_root.findall('ZAP'):
                for pac in element.findall('PACIENT'):
                    idpac = pac.find('ID_PAC').text
                    vpolis = pac.find('VPOLIS').text
                    spolis = convert_none_type(pac.find('SPOLIS'))
                    npolis = pac.find('NPOLIS').text
                    stokato = pac.find('ST_OKATO').text
                    smo = convert_none_type(pac.find('SMO'))
                    smoogrn = convert_none_type(pac.find('SMO_OGRN'))
                    smook = convert_none_type(pac.find('SMO_OK'))
                    smonam = convert_none_type(pac.find('SMO_NAM'))
                    novor = pac.find('NOVOR').text
                    vnov_d = convert_none_type(pac.find('VNOV_D'))

                    # insert_pacient(glpu, idpac, vpolis, spolis, npolis,
                    #                stokato, smo, smoogrn, smook, smonam, novor, vnov_d)
                    try:
                        queryPT = dbcur.prepare('INSERT INTO PT05S502018051_COPY (glpu, id_pac, vpolis, spolis, npolis, smo,'
                                                'smo_ogrn, smo_ok, smo_nam, novor, vnov_d, polis) '
                                                'VALUES (:glpu, :idpac, :vpolis, :spolis, :npolis, :smo, '
                                                ':smoogrn, :smook, :smonam, :novor, :vnov_d, :polis_pac)')

                        polis_pac = spolis.strip() + npolis.strip()
                        dbcur.execute(queryPT, (glpu, idpac, vpolis, spolis, npolis, smo, smoogrn, smook,
                                              smonam, novor, vnov_d, polis_pac))

                    except cx_Oracle.Error as err:
                        print(f'Query error: {err}')

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
                    sank_it = float(slu.find('SANK_IT').text)
                    tal_d = convert_none_type(slu.find('TAL_D'))
                    tal_p = convert_none_type(slu.find('TAL_P'))
                    vbr = convert_none_type(slu.find('VBR'))
                    p_otk = convert_none_type(slu.find('P_OTK'))
                    nrisoms = slu.find('NRISOMS').text
                    ds1_pr = slu.find('DS1_PR').text
                    ds4 = slu.find('DS4').text
                    nazn = slu.find('NAZN').text
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
                    smo_sl = slu.find('SMO').text

                    # insert_sluch(lpu, lpu_1, idcase, usl_ok, vidpom, for_pom, disp, vid_hmp, metod_hmp,
                    #              npr_mo, extr, podr, profil, det, nhistory, date_1, date_2, ds0, ds1,
                    #              ds2, ds3, vnov_m, code_mes1, code_mes2, rslt, rslt_d, ishod, prvs, vers_spec,
                    #              iddokt, os_sluch, idsp, ed_col, tarif, sumv, oplata, sump, sank_it, tal_d,
                    #              tal_p, vbr, p_otk, nrisoms, ds1_pr, ds4, nazn, naz_sp, naz_v, naz_pmp,
                    #              naz_pk, pr_d_n, comentsl, pr_nov, novor_sl, orders, t_order, kem_prov, smo_sl)

                    queryTT = dbcur.prepare('INSERT INTO TT05S50201805_COPY (glpu, mcod, idcase, usl_ok, vidpom, for_pom, '
                                'disp, vid_hmp, metod_hmp, npr_mo, extr, podr, profil, det, nhistory, date_1,'
                                'date_2, ds0, ds1, ds2, ds3, vnov_m, code_mes1, code_mes2, rslt, rslt_d, '
                                'ishod, prvs, vers_spec, iddokt, os_sluch, idsp, ed_col, tarif, sumv, '
                                'oplata, sump, tal_d, tal_p, vbr, p_otk, nrisoms, ds1_pr, ds4, nazn, naz_sp, '
                                'naz_v, naz_pmp, naz_pk, pr_d_n, comentsl, pr_nov, novor, order_, t_order, '
                                'kem_prov, smo, id_sluch_tt, prizn_prov) '
                                'VALUES (:lpu, :lpu_1, :idcase, :usl_ok, :vidpom, :for_pom, :disp, '
                                ':vid_hmp, :metod_hmp, :npr_mo, :extr, :podr, :profil, :det, :nhistory, '
                                ':dt1, :dt2, :ds0, :ds1, :ds2, :ds3, :vnov_m, :code_mes1, :code_mes2, '
                                ':rslt, :rslt_d, :ishod, :prvs, :vers_spec, :iddokt, :os_sluch, :idsp, '
                                ':ed_col, :tarif, :sumv, :oplata, :sump, :dtd, :dtp, :vbr, :p_otk, '
                                ':nrisoms, :ds1_pr, :ds4, :nazn, :naz_sp, :naz_v, :naz_pmp, :naz_pk, '
                                ':pr_d_n, :comentsl, :pr_nov, :novor_sl, :orders, :t_order,:kem_prov, '
                                ':smo_sl, :ids, :prizn_prov)')

                    dt1 = datetime.strptime(date_1, "%Y-%m-%d")
                    dt2 = datetime.strptime(date_2, "%Y-%m-%d")

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
                                idcase, 0))

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
                        koef_k = float(usl.find('KOEF_K').text)
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
                        stand = usl.find('STAND').text
                        p_per = usl.find('P_PER').text
                        npl = usl.find('NPL').text
                        idsh = convert_none_type(usl.find('idsh'))

                        # insert_usl(lpu_u, lpu_1u, idcase, idserv, podr, profil_u, det,
                        #            date_in, date_out, ds, code_usl,
                        #            ed_col_u, koef_k, pouh, zak, kol_usl, tarif, sumv_usl,
                        #            prvs, code_md, comentu, dir2, gr_zdorov, student,
                        #            spolis_u, npolis_u, stand, p_per, npl, idsh)

                        query = dbcur.prepare('INSERT INTO UT05S50201805_COPY (lpu, lpu_1, ID_SLUCH, idserv, podr, profil,'
                                              'det, date_in, date_out, ds, code_usl, ed_col, koefk, pouh, zak, kol_usl, '
                                              'tarif, sumv_usl, prvs_u, code_md, comentu, dir2, gr_zdorov, student, spolis, '
                                              'npolis, stand, p_per, npl, idsh) '
                                              'VALUES (:lpu_u, :lpu_1u, :idcase, :idserv, :podr, :profil_u, :det, '
                                              ':date_in, :date_out, :ds, :code_usl, :ed_col_u, :koef_k, :pouh, :zak, '
                                              ':kol_usl, :tarif, :sumv_usl, :prvs, :code_md, :comentu, :dir2, :gr_zdorov, '
                                              ':student, :spolis_u, :npolis_u, :stand, :p_per, :npl, :idsh)')

                        dtin = datetime.strptime(date_in, "%Y-%m-%d")
                        dtout = datetime.strptime(date_out, "%Y-%m-%d")
                        dbcur.execute(query, (lpu_u, lpu_1u, idcase, idserv, podr, profil_u, det, dtin, dtout,
                                              ds, code_usl, ed_col_u, koef_k, pouh, zak, kol_usl, tarif,
                                              sumv_usl, prvs, code_md, comentu, dir2, gr_zdorov, student,
                                              spolis_u, npolis_u, stand, p_per, npl, idsh))

                        for vmp_oper in usl.findall('HRRGD'):
                            vid_vme = vmp_oper.find('VID_VME').text
                            ksgh = vmp_oper.find('KSGH').text
                            idnomk = vmp_oper.find('IDNOMK').text
                            name_o = vmp_oper.find('NAME_O').text

                            # insert_oper(lpu_u, lpu_1u, idserv, vid_vme, ksgh, idnomk, name_o)

                            query = dbcur.prepare('INSERT INTO NT05S50201805_COPY (glpu, mcod, idserv, hkod, ksgh, idnomk, name_o) '
                                                  'values (:glpu, :mcod, :idserv, :hkod, :ksgh, :idnomk, :name_o)')

                            dbcur.execute(query, (lpu, lpu_1, idserv, vid_vme, ksgh, idnomk, name_o))

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

                # insert_schet(code, code_mo, year_s, month_s, nschet, dschet, plat, summav, coments, summap)

                queryST = dbcur.prepare('INSERT INTO ST05S50201805_COPY (code, glpu, yer, mont, nschet, dschet, plat, '
                                        'summav, coments, summap) '
                                        'VALUES (:code, :glpu, :year_s, :month_s, :nschet, :dt, :plat, '
                                        ':summav, :coments, :summap)')

                dt = datetime.strptime(dschet, "%Y-%m-%dT%H:%M:%S").date()
                dbcur.execute(queryST, (code, code_mo, year_s, month_s, nschet, dt, plat, summav, coments, summap))

            for element_doc in element_xml_root.findall('VRACH'):
                kod = element_doc.find('KOD').text
                fio = element_doc.find('FIO').text
                mcod = element_doc.find('LPU_1').text
                idmsp = element_doc.find('IDMSP').text
                spec = convert_none_type(element_doc.find('SPEC'))

                # insert_doc(glpu, mcod, kod, fio, idmsp, spec)

                queryDT = dbcur.prepare('INSERT INTO DT05S50201805_COPY (glpu, mcod, kod, fio, idmsp, spec) '
                                        'VALUES (:glpu, :mcod, :kod, :fio, :idmsp, :spec)')
                dbcur.execute(queryDT, (glpu, mcod, kod, fio, idmsp, spec))

            db.commit()
            dbcur.close()

        if xml[0] == 'L':
            year = '20' + xml[8:10]
            month = xml[10:12]
            glpu_l = xml[12:18]

            db = con('db')
            dbcur = db.cursor()
            element_xml_root = tree.getroot()
            for elem_pers in element_xml_root.findall('PERS'):
                id_pac = convert_none_type(elem_pers.find('ID_PAC'))
                fam = convert_none_type(elem_pers.find('FAM'))
                im = convert_none_type(elem_pers.find('IM'))
                ot = convert_none_type(elem_pers.find('OT'))
                w = elem_pers.find('W').text
                dr = elem_pers.find('DR').text
                dost = elem_pers.find('DOST').text
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
                okatog = elem_pers.find('OKATOG').text
                okatop = elem_pers.find('OKATOP').text
                adres = convert_none_type(elem_pers.find('ADRES'))
                ident_sp = convert_none_type(elem_pers.find('IDENT_SP'))
                comentp = elem_pers.find('COMENTP').text
                vpolis = elem_pers.find('VPOLIS').text
                novor = elem_pers.find('NOVOR').text

                    # insert_pacpers(glpu, id_pac, fam, im, ot, w, dr, dost, fam_p, im_p, ot_p, dr_p,
                    #            dost_p, w_p, mr, doctype, docser, docnum, snils, okatog,
                    #            okatop, adres, ident_sp, comentp, vpolis, novor)

                query = dbcur.prepare('UPDATE PT05S502018051_COPY '
                                      'SET fam = :fam, im = :im, ot = :ot, w = :w, dr = :dr, dost = :dost, '
                                      'fam_p = :fam_p, im_p = :im_p, ot_p = :ot_p, dr_p = :dr_p, dost_p = :dost_p, '
                                      'w_p = :w_p, mr = :mr, doctype = :doctype, docser = :docser, docnum = :docnum, '
                                      'snils = :snils, adres = :adres, ident_sp = :ident_sp '
                                      'WHERE id_pac = :id_pac and glpu = :glpu_l')

                dr1 = datetime.strptime(dr, "%Y-%m-%d")
                if dr_p == '':
                    dr2_p = datetime.strptime('1900-01-01', "%Y-%m-%d")
                else:
                    dr2_p = datetime.strptime(dr_p, "%Y-%m-%d")
                dbcur.execute(query, (fam, im, ot, w, dr1, dost, fam_p, im_p, ot_p, dr2_p,
                                  dost_p, w_p, mr, doctype, docser, docnum, snils,
                                  adres, ident_sp, id_pac, glpu_l))

            db.commit()
            dbcur.close()

        os.remove(path + '\\' + xml)

    except IOError as err:
        print(err)


"""
Функция получения наименования XML файлов из zip архива
"""
def getFileXml(xml_file, year, month, glpu):
    # if os.path.isfile(xml_file) and os.access(xml_file, os.R_OK):
    try:
        pathxml = os.path.dirname(xml_file)
        typefile = os.path.basename(xml_file)[-5]
        files = os.listdir(pathxml)
        xml = filter(lambda x: x.endswith(year[2:4] + month + glpu + typefile + '.XML'), files)
        DeleteFromDB(glpu)

        for file in xml:
            XmlToDB(pathxml, file)

    except IOError as err:
        print(err)