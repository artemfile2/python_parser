# -*- coding: utf-8 -*-

import locale

import xlrd
from xlwt import *
from xlutils.copy import copy
from connect import *


def export_xls(period, glpu):
    """

    * Colour index
    8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta,
    7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown),
    20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on... sty

    * Borders
    borders.left, borders.right, borders.top, borders.bottom
    May be: NO_LINE, THIN, MEDIUM, DASHED, DOTTED, THICK, DOUBLE, HAIR, MEDIUM_DASHED,
    THIN_DASH_DOTTED, MEDIUM_DASH_DOTTED, THIN_DASH_DOT_DOTTED, MEDIUM_DASH_DOT_DOTTED,
    SLANTED_MEDIUM_DASH_DOTTED, or 0x00 through 0x0D.

    borders = xlwt.Borders()
    borders.left = xlwt.Borders.THIN
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    borders.bottom = xlwt.Borders.THIN
    borders.left_colour = 0x00
    borders.right_colour = 0x00
    borders.top_colour = 0x00
    borders.bottom_colour = 0x00
    style.borders = borders

    * Fonts
    style.font = xlwt.Font()
    style.font.height = 8 * 20
    style.font.colour_index = 22

    * Alignment
    style.alignment = xlwt.Alignment()
    style.alignment.horz = xlwt.Alignment.HORZ_LEFT
    style.alignment.vert = xlwt.Alignment.VERT_CENTER

    * Pattern
    May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12

    style.pattern = xlwt.Pattern()
    style.pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    style.pattern.pattern_fore_colour = 23

    """
    print('start xls')
    db = con('db')
    dbcur = db.cursor()

    query_data = dbcur.prepare('SELECT x_pac.FAM ||'+"' '" +'|| x_pac.IM ||'+"' '" +'|| x_pac.OT as fio, SNK.COMMENTS, Snk.ID_PAC, '
                               'Snk.MCOD, Snk.POVOD, X_PAC.DR, x_pac.ADRES, X_USL.DATE_IN, X_USL.DATE_OUT, ' 
                               'X_USL.DS, X_USL.CODE_USL, X_USL.TARIF, X_USL.SUMV_USL, Snk.SUMM_SHTR, ' 
                               '(X_USL.SUMV_USL-Snk.SUMM_SHTR) as oplata '       
                               'FROM SANKC Snk ' 
                               'INNER JOIN (SELECT XU.LPU, XU.IDSERV, XU.SUMV_USL, XU.PODR, XU.DATE_IN, XU.DATE_OUT, '
                               'XU.DS, XU.CODE_USL, XU.TARIF, XU.PERIOD prd '
                               'FROM XML_USL XU '
                               'WHERE XU.PERIOD = TO_DATE(:period, '+"'dd.mm.YYYY'"+')) x_usl ' 
                               'ON SNK.IDSERV = x_usl.IDSERV AND SNK.GLPU = X_USL.LPU ' 
                               'AND TO_DATE(SNK.PERIOD, '+"'dd.mm.YYYY'"+') = X_USL.PRD ' 
                               'LEFT JOIN (SELECT XP.GLPU, XP.VPOLIS, XP.NOVOR, XP.FAM, XP.IM, XP.OT, XP.W, ' 
                               'XP.DR, XP.ID_PAC, xp.PERIOD prd, xp.ADRES ' 
                               'FROM XML_PACIENT XP '
                               'WHERE XP.PERIOD = TO_DATE(:period, '+"'dd.mm.YYYY'"+')) x_pac ' 
                               'ON SNK.GLPU = x_pac.GLPU AND snk.ID_PAC = X_PAC.ID_PAC AND ' 
                               'TO_DATE(SNK.PERIOD, '+"'dd.mm.YYYY'"+') = X_PAC.PRD ' 
                               'WHERE Snk.GLPU = :glpu AND Snk.PERIOD = :period')
    dbcur.execute(query_data, (period, period, glpu, period))
    data_glpu = dbcur.fetchall()

    query_mcod = dbcur.prepare('SELECT DISTINCT "s".MCOD, TRIM("sl".NAME) names FROM SANKC "s" '
                               'LEFT JOIN S_LPU "sl" '
                               'ON "s".MCOD = "sl".MCOD '
                               'WHERE "s".GLPU = :glpu AND "s".PERIOD = :period '
                               'ORDER BY "s".MCOD ')
    dbcur.execute(query_mcod, (glpu, period))
    data_namelpu = dbcur.fetchall()

    query_povod = dbcur.prepare('SELECT DISTINCT "s".POVOD, TRIM("p".NAME1) names FROM SANKC "s" '
                                'LEFT JOIN POVOD "p" '
                                'ON "s".POVOD = "p".KOD '  
                                'WHERE "s".GLPU = :glpu AND "s".PERIOD = :period '
                                'ORDER BY "s".POVOD ')
    dbcur.execute(query_povod, (glpu, period))
    data_povod = dbcur.fetchall()

    query_namemo = dbcur.prepare('SELECT "sl".M_NAMEF FROM S_LPU "sl" '
                                 'WHERE "sl".MCOD = :glpu ')
    dbcur.execute(query_namemo, (glpu, ))
    namemo = dbcur.fetchall()

    query_sumpred = dbcur.prepare('SELECT SUM("xu".SUMV_USL) sm_oms, "pdn".SUMP pdn, "sp".SUM smp, "pdn".OT_MES FROM XML_USL "xu" '
                                  'LEFT JOIN (SELECT * FROM PODUSH '
                                  'WHERE SMO = '+"'05501'"+' AND OT_MES = TO_NUMBER(SUBSTR(:period, 4,2)) ' 
                                  'AND OT_GOD = TO_NUMBER(SUBSTR(:period, 7,4))) "pdn" '
                                  'ON "xu".LPU = "pdn".GLPU '
                                  'LEFT JOIN (SELECT * FROM SMP '
                                  'WHERE MONTH = TO_NUMBER(SUBSTR(:period, 4,2)) '
                                  'AND YEAR = TO_NUMBER(SUBSTR(:period, 7,4))) "sp" '
                                  'ON "xu".LPU = "sp".GLPU '
                                  'WHERE "xu".LPU = :glpu AND "xu".PERIOD = TO_DATE(:period, '+"'dd.mm.yyyy'"+') '
                                  'GROUP BY "pdn".SUMP, "pdn".OT_MES, "sp".SUM '
                                  'ORDER BY "pdn".OT_MES ')
    dbcur.execute(query_sumpred, (period, period, period, period, glpu, period))
    predsum = dbcur.fetchall()

    dbcur.close()

    borders = Borders()
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1

    fnt = Font()
    fnt.name = 'Calibri'
    fnt.height = 20*24
    fnt.bold = True
    fnt.colour_index = 4
    styleHeader = XFStyle()
    styleHeader.font = fnt
    pattern = Pattern()
    pattern.pattern = Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = Style.colour_map['ivory']
    styleHeader.pattern = pattern

    fnt = Font()
    fnt.name = 'Calibri'
    fnt.height = 20 * 24
    fnt.bold = True
    fnt.colour_index = 0
    styleDay = XFStyle()
    styleDay.font = fnt
    styleDay.alignment = Alignment()
    styleDay.alignment.horz = Alignment.HORZ_CENTER
    pattern = Pattern()
    pattern.pattern = Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = Style.colour_map['gray25']
    styleDay.pattern = pattern

    fnt = Font()
    fnt.name = 'Calibri'
    fnt.height = 20 * 11
    fnt.bold = True
    fnt.colour_index = 0
    styleDate = XFStyle()
    styleDate.font = fnt
    styleDate.alignment = Alignment()
    styleDate.alignment.horz = Alignment.HORZ_CENTER
    pattern = Pattern()
    pattern.pattern = Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = Style.colour_map['gray25']
    styleDate.pattern = pattern

    fnt = Font()
    fnt.name = 'Calibri'
    fnt.height = 20 * 13
    fnt.bold = True
    fnt.colour_index = 0
    styleTime = XFStyle()
    styleTime.font = fnt
    styleTime.alignment = Alignment()
    styleTime.alignment.horz = Alignment.HORZ_CENTER
    pattern = Pattern()
    pattern.pattern = Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = Style.colour_map['aqua']
    styleTime.pattern = pattern

    fnt = Font()
    fnt.name = 'Calibri'
    fnt.height = 20 * 13
    fnt.bold = True
    fnt.colour_index = 0
    styleB = XFStyle()
    styleB.font = fnt
    styleB.alignment = Alignment()
    styleB.alignment.horz = Alignment.HORZ_CENTER
    styleB.borders = borders
    pattern = Pattern()
    pattern.pattern = Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = Style.colour_map['ivory']
    styleB.pattern = pattern

    fnt = Font()
    fnt.name = 'Calibri'
    fnt.height = 20 * 11
    fnt.bold = True
    fnt.colour_index = 0
    styleText = XFStyle()
    styleText.font = fnt
    styleText.borders = borders

    wb = Workbook()
    ws = wb.add_sheet('МЭК')

    locale.setlocale(locale.LC_ALL, "")
    ws.write_merge(0, 1, 0, 4, 'РЕЗУЛЬТАТ МЭК АО "МАКС-М"', styleHeader)
    ws.write(1, 7, 'Дата файла')
    ws.write(2, 4, datetime.now().day, styleDay)
    ws.write(2, 5, datetime.now().strftime("%B"), styleDate)
    ws.write(2, 6, datetime.now().year, styleDate)
    ws.write(2, 7, datetime.now().strftime("(%A)"), styleDate)
    ws.write(2, 8, datetime.now().time().strftime('%H:%M:%S'), styleTime)

    ot_mes = datetime.strptime(period, '%d.%m.%Y').strftime("%B %Y")
    ws.write_merge(3, 3, 0, 3, 'МЭК счетов за отчетный месяц {}'.format(ot_mes), styleHeader)
    ws.write_merge(5, 5, 0, 12, 'Наименование МО: {0} {1}'.format(glpu, namemo[0][0]), styleHeader)
    ws.write_merge(6, 6, 0, 6,
                   f'Cумма ОМС по счетам: {predsum[0][0]};  '
                   f'в т.ч. пдн: {predsum[0][1] if predsum[0][1] else 0};  '
                   f'в т.ч смп: {predsum[0][2] if predsum[0][2] else 0}',
                   styleHeader)

    ws.write(8, 0, 'Код МО', styleB)
    ws.write(8, 1, 'Наименование подразделения', styleB)
    num_mcod = 9
    for mcodname in data_namelpu:
        ws.write(num_mcod, 0, mcodname[0], styleText)  # mcod
        ws.write(num_mcod, 1, mcodname[1], styleText)  # name
        num_mcod += 1

    num_pov = num_mcod + 2
    ws.write(num_pov, 0, 'Код деф', styleB)
    ws.write(num_pov, 1, 'Наименование дефекта', styleB)
    num_pov += 1
    for povod in data_povod:
        ws.write(num_pov, 0, povod[0], styleText)  # mcod
        ws.write(num_pov, 1, povod[1], styleText)  # name
        num_pov += 1

    i = num_pov + 2
    ws.write(i, 0, '№ п/п', styleB)
    ws.write(i, 1, 'Ф.И.О.', styleB)
    ws.write(i, 2, 'Выявленный дефект', styleB)
    ws.write(i, 3, 'Полис', styleB)
    ws.write(i, 4, 'Код МО', styleB)
    ws.write(i, 5, 'Код дефекта', styleB)
    ws.write(i, 6, 'Дата рожд.', styleB)
    ws.write(i, 7, 'Адрес', styleB)
    ws.write(i, 8, 'Дата нач.лечения', styleB)
    ws.write(i, 9, 'Дата окон.лечения', styleB)
    ws.write(i, 10, 'Код МКБ', styleB)
    ws.write(i, 11, 'Код услуги', styleB)
    ws.write(i, 12, 'Кол. усл.', styleB)
    ws.write(i, 13, 'Тариф', styleB)
    ws.write(i, 14, 'Сумма лечения', styleB)
    ws.write(i, 15, 'Сумма штрафа', styleB)
    ws.write(i, 16, 'Оплата', styleB)
    i += 1
    for cnt, data in enumerate(data_glpu, 1):
        ws.write(i, 0, str(cnt), styleText)  # №
        ws.write(i, 1, data[0], styleText)  # ФИО
        ws.write(i, 2, data[1], styleText)  # наименование дефекта
        ws.write(i, 3, data[2][0:-2], styleText)  # полис
        ws.write(i, 4, data[3], styleText)  # код МО
        ws.write(i, 5, data[4], styleText)  # код дефекта
        ws.write(i, 6, data[5].strftime('%d.%m.%Y'), styleText)  # дата рождения
        ws.write(i, 7, data[6], styleText)  # адрес
        ws.write(i, 8, data[7].strftime('%d.%m.%Y'), styleText)  # дата начала лечения
        ws.write(i, 9, data[8].strftime('%d.%m.%Y'), styleText)  # дата конца лечения
        ws.write(i, 10, data[9], styleText)
        ws.write(i, 11, data[10], styleText)
        ws.write(i, 12, '1', styleText)
        ws.write(i, 13, data[11], styleText)
        ws.write(i, 14, data[12], styleText)
        ws.write(i, 15, data[13], styleText)
        ws.write(i, 16, data[14], styleText)
        i += 1

    ws.col(1).width = 12000
    ws.col(2).width = 11000
    ws.col(3).width = 4500
    ws.col(4).width = 2500
    ws.col(5).width = 3500
    ws.col(6).width = 3000
    ws.col(7).width = 13000
    ws.col(8).width = 3500
    ws.col(9).width = 3500
    ws.col(10).width = 3500
    ws.col(11).width = 3000
    ws.col(12).width = 2500
    ws.col(13).width = 4500
    ws.col(14).width = 4500
    ws.col(15).width = 4500
    ws.col(16).width = 4500

    wb.save(r'C:\txt\es50m{0}_{1}.xls'.format(glpu, period[8:] + period[3:5]))
    print('END  xls')
