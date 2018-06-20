import cx_Oracle
import os
from datetime import *

def con(type = 'cur'):
    # Выполняем подключение с отловом ошибок
    try:

        os.environ["NLS_LANG"] = "Russian.AL32UTF8"
        db = cx_Oracle.connect("SYSTEM", "Q1234567890", "192.168.1.209/ORCL")

        dbcur = db.cursor()
        if type == 'cur':
            return dbcur
        else:
            return db

    except cx_Oracle.Error as error:
        print("Ошибка подключения: '" + str(error) + "'.")


def get_glpu():
    try:
        dbcur = con()
        query = dbcur.prepare('SELECT sg.GLPU, sg.MCOD, sg.NAME, sg.M_NAMEF, sg.IDUMP FROM S_LPU sg '
                              'INNER JOIN (SELECT DISTINCT glpu FROM S_LPU WHERE glpu <> {!r}) sl '
                              'ON sg.MCOD = sl.GLPU '
                              'ORDER BY sg.GLPU'.format('054503'))
        dbcur.execute(query)

        # Получаем данные.
        glpu = dbcur.fetchall()

        # Разрываем подключение.
        dbcur.close()
        return glpu

    except cx_Oracle.Error as err:
        print("Query error: {}".format(err))

def get_slpu():
    try:
        dbcur = con()
        dbcur.execute("SELECT glpu, mcod, name, m_namef, idump FROM s_lpu order by glpu")

        # Получаем данные.
        slpu = dbcur.fetchall()

        dbcur.close()
        return slpu

    except cx_Oracle.Error as err:
        print("Query error: {}".format(err))

def get_slpuonglpu(glpu):
    try:
        dbcur = con()
        query = dbcur.prepare('SELECT glpu, mcod, name, m_namef, idump FROM s_lpu WHERE glpu = :lpu')
        dbcur.execute(query, {'lpu': glpu})

        slpu = dbcur.fetchone()
        dbcur.close()
        return slpu

    except cx_Oracle.Error as err:
        print("Query error: {}".format(err))

"""
Функция добавления записей врачей из XML в базу
"""
def insert_doc(glpu, mcod, kod, fio, idmsp, spec):
    try:
        db = con('db')
        dbcur = db.cursor()
        #doctor
        query = dbcur.prepare('INSERT INTO DT05S50201805_COPY (glpu, mcod, kod, fio, idmsp, spec) '
                              'VALUES (:glpu, :mcod, :kod, :fio, :idmsp, :spec)')
        dbcur.execute(query, (glpu, mcod, kod, fio, idmsp, spec))
        db.commit()
        dbcur.close()

    except cx_Oracle.Error as err:
        print("Query error: {}".format(err))


"""
Функция добавления записи счета из XML в базу
"""
def insert_schet(code, code_mo, year, month, nschet, dschet, plat, summav, coments, summap):
    try:
        db = con('db')
        dbcur = db.cursor()
        #schet
        query = """INSERT INTO ST05S50201805_COPY (code, glpu, yer, mont, nschet, dschet, plat, summav, coments, summap) 
                   VALUES (:code, :glpu, :yer, :mont, :nschet, :dt, :plat, :summav, :coments, :summap)"""

        dt = datetime.strptime(dschet, "%Y-%m-%dT%H:%M:%S").date()
        dbcur.execute(query, (code, code_mo, year, month, nschet, dt, plat, summav, coments, summap))
        # db.commit()
        # dbcur.close()

    except cx_Oracle.Error as err:
        print("Query error: {}".format(err))


"""
Функция добавления записи пациентов из XML в базу
"""
def insert_pacient(glpu, id_pac, vpolis, spolis, npolis,
                 st_okato, smo, smoogrn, smo_ok, smo_nam, novor, vnov_d):

    try:
        db = con('db')
        dbcur = db.cursor()
        # polis

        query = """INSERT INTO PT05S50201805_COPY (glpu, id_pac, vpolis, spolis, npolis, smo, smo_ogrn, smo_ok,
                   smo_nam, novor, vnov_d, polis) 
                   VALUES (:glpu, :id_pac, :vpolis, :spolis, :npolis, :smo, :smoogrn, :smo_ok,
                   :smo_nam, :novor, :vnov_d, :polis_pac)"""

        polis_pac = spolis.strip() + npolis.strip()
        dbcur.execute(query, (glpu, id_pac, vpolis, spolis, npolis, smo, smoogrn, smo_ok,
                              smo_nam, novor, vnov_d, polis_pac))

        # db.commit()
        # dbcur.close()

    except cx_Oracle.Error as err:
        print(f'Query error: {err}')


"""
Функция добавления записи персональных данных пациентов из XML в базу
"""
def insert_pacpers(glpu, id_pac, fam, im , ot , w, dr, dost, fam_p, im_p, ot_p, dr_p,
                   dost_p, w_p, mr, doctype, docser, docnum, snils, okatog,
                   okatop, adres, ident_sp, comentp, vpolis, novor):
    try:
        db = con('db')
        dbcur = db.cursor()

        query = """UPDATE PT05S50201805_COPY 
                   SET fam = :fam, im = :im, ot = :ot, w = :w, dr = :dr, dost = :dost, 
                       fam_p = :fam_p, im_p = :im_p, ot_p = :ot_p, dr_p = :dr_p, 
                       dost_p = :dost_p, w_p = :w_p, mr = :mr, doctype = :doctype, 
                       docser = :docser, docnum = :docnum, snils = :snils, adres = :adres, 
                       ident_sp = :ident_sp
                   WHERE id_pac = :id_pac"""

        dr1 = datetime.strptime(dr, "%Y-%m-%d")
        if dr_p == '':
            dr2_p = datetime.strptime('1900-01-01', "%Y-%m-%d")
        else:
            dr2_p = datetime.strptime(dr_p, "%Y-%m-%d")
        dbcur.execute(query, (fam, im, ot, w, dr1, dost, fam_p, im_p, ot_p, dr2_p,
                              dost_p, w_p, mr, doctype, docser, docnum, snils,
                              adres, ident_sp, id_pac))

        # db.commit()
        # dbcur.close()

    except cx_Oracle.Error as err:
        print("Query error: {}".format(err))



"""
Функция добавления записи случаев SLUCH пациентов из XML в базу
"""
def insert_sluch(lpu, lpu_1, idcase, usl_ok, vidpom, for_pom, disp, vid_hmp,
                 metod_hmp, npr_mo, extr, podr, profil, det, nhistory, date_1, date_2, ds0,
                 ds1, ds2, ds3, vnov_m, code_mes1, code_mes2, rslt, rslt_d, ishod, prvs,
                 vers_spec, iddokt, os_sluch, idsp, ed_col, tarif, sumv, oplata, sump,
                 sank_it, tal_d, tal_p, vbr, p_otk, nrisoms, ds1_pr, ds4, nazn, naz_sp,
                 naz_v, naz_pmp, naz_pk, pr_d_n, comentsl, pr_nov, novor_sl, orders,
                 t_order, kem_prov, smo_sl):
    try:
        db = con('db')
        dbcur = db.cursor()

        query = """INSERT INTO TT05S50201805_COPY (glpu, mcod, idcase, usl_ok, vidpom, for_pom,  
                   disp, vid_hmp, metod_hmp, npr_mo, extr, podr, profil, det, nhistory,
                   date_1, date_2, ds0, ds1, ds2, ds3, vnov_m, code_mes1, code_mes2, rslt,
                   rslt_d, ishod, prvs, vers_spec, iddokt, os_sluch, idsp, ed_col, tarif,
                   sumv, oplata, sump, tal_d, tal_p, vbr, p_otk, nrisoms, ds1_pr,
                   ds4, nazn, naz_sp, naz_v, naz_pmp, naz_pk, pr_d_n, comentsl, pr_nov,
                   novor, order_, t_order, kem_prov, smo,
                   id_sluch_tt,  prizn_prov) 
                   values (:glpu, :mcod, :idcase, :usl_ok, :vidpom, :for_pom,
                     :disp, :vid_hmp, :metod_hmp, :npr_mo, :extr, :podr, :profil,
                     :det, :nhistory, :date_1, :date_2, :ds0, :ds1, :ds2, :ds3, 
                     :vnov_m, :code_mes1, :code_mes2, :rslt, :rslt_d, :ishod, :prvs, :vers_spec,
                     :iddokt, :os_sluch, :idsp, :ed_col, :tarif, :sumv, :oplata, :sump,
                     :tal_d, :tal_p, :vbr, :p_otk, :nrisoms, :ds1_pr, 
                     :ds4, :nazn, :naz_sp, :naz_v, :naz_pmp, :naz_pk, :pr_d_n, :comentsl, :pr_nov,
                     :novor_sl, :orders,: t_order,:kem_prov,: smo_sl,
                     :ids, :prizn_prov)"""

        ids = lpu_1 + ' id ' + nhistory.strip()
        dt1 = datetime.strptime(date_1, "%Y-%m-%d")
        dt2 = datetime.strptime(date_2, "%Y-%m-%d")
        dtd = datetime.strptime(tal_d, "%Y-%m-%d")
        dtp = datetime.strptime(tal_p, "%Y-%m-%d")
        prizn_prov = 0
        dbcur.execute(query, (lpu, lpu_1, idcase, usl_ok, vidpom, for_pom, disp, vid_hmp,
         metod_hmp, npr_mo, extr, podr, profil, det, nhistory, dt1, dt2, ds0,
         ds1, ds2, ds3, vnov_m, code_mes1, code_mes2, rslt, rslt_d, ishod, prvs,
         vers_spec, iddokt, os_sluch, idsp, ed_col, tarif, sumv, oplata, sump,
         dtd, dtp, vbr, p_otk, nrisoms, ds1_pr, ds4, nazn, naz_sp, naz_v, naz_pmp,
         naz_pk, pr_d_n, comentsl, pr_nov, novor_sl, orders, t_order, kem_prov, smo_sl,
         ids, prizn_prov))

        # db.commit()
        # dbcur.close()

    except cx_Oracle.Error as err:
        print("Query error: {}".format(err))


"""
Функция добавления записи услуг пациентов из XML в базу
"""
def insert_usl(lpu_u, lpu_1u, idcase, idserv, podr, profil_u, det, date_in,
               date_out , ds , code_usl, ed_col_u, koef_k, pouh, zak, kol_usl,
               tarif, sumv_usl, prvs, code_md, comentu, dir2, gr_zdorov, student,
               spolis_u, npolis_u, stand, p_per, npl, idsh):
    try:
        db = con('db')
        dbcur = db.cursor()

        query = """INSERT INTO UT05S50201805_COPY 
                    (lpu, lpu_1, ID_SLUCH, idserv, podr, profil, det, date_in, date_out,
                     ds, code_usl, ed_col, koefk, pouh, zak, kol_usl, tarif, 
                     sumv_usl, prvs_u, code_md, comentu, dir2, gr_zdorov, student,
                     spolis, npolis, stand, p_per, npl, idsh) 
                   values (:lpu_u, :lpu_1u, :idcase, :idserv, :podr, :profil_u, :det,
                    :date_in, :date_out, :ds, :code_usl, :ed_col_u, :koef_k, :pouh , :zak,
                    :kol_usl, :tarif, :sumv_usl, :prvs, :code_md, :comentu, :dir2, :gr_zdorov,
                    :student, :spolis_u, :npolis_u, :stand, :p_per, :npl, :idsh)"""

        #
        dtin = datetime.strptime(date_in, "%Y-%m-%d")
        dtout = datetime.strptime(date_out, "%Y-%m-%d")
        dbcur.execute(query, (lpu_u, lpu_1u, idcase, idserv, podr, profil_u, det, dtin, dtout,
                              ds, code_usl, ed_col_u, koef_k, pouh, zak, kol_usl, tarif,
                              sumv_usl, prvs, code_md, comentu, dir2, gr_zdorov, student,
                              spolis_u, npolis_u, stand, p_per, npl, idsh))

        # db.commit()
        # dbcur.close()

    except cx_Oracle.Error as err:
        print(f'Query error: {err}')

"""
Функция добавления записи счета из XML в базу
"""
def insert_oper(lpu, lpu_1, idserv, vid_vme, ksgh, idnomk, name_o):
    try:
        db = con('db')
        dbcur = db.cursor()
        query = """INSERT INTO NT05S50201805_COPY (glpu, mcod, idserv, hkod, ksgh, idnomk, name_o)
                   values (:glpu, :mcod, :idserv, :hkod, :ksgh, :idnomk, :name_o)"""

        dbcur.execute(query, (lpu, lpu_1, idserv, vid_vme, ksgh, idnomk, name_o))
        # db.commit()
        # dbcur.close()

    except cx_Oracle.Error as err:
        print("Query error: {}".format(err))




def commitDB():
    db = con('db')
    # dbcur = db.cursor()
    db.commit()