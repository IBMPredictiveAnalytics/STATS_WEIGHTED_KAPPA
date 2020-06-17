#/***********************************************************************
# * Licensed Materials - Property of IBM
# *
# * IBM SPSS Products: Statistics Common
# *
# * (C) Copyright IBM Corp. 1989, 2020
# *
# * US Government Users Restricted Rights - Use, duplication or disclosure
# * restricted by GSA ADP Schedule Contract with IBM Corp.
# ************************************************************************/
__author__ = "SPSS, DPN"
__version__ = "1.2.1"

import tempfile, spss, spssaux, random
from extension import Template, Syntax, checkrequiredparams, processcmd
from spssaux import _smartquote
from spss import CellText

def Run(args):
    """Execute the STATS WEIGHTED KAPPA command"""

    args = args[list(args.keys())[0]]

    oobj = Syntax([
        Template("VARIABLES", subc="",  ktype="existingvarlist", var="variables", islist=True),
        Template("WTTYPE", subc="OPTIONS",  ktype="int", var="wttype"),
        Template("CILEVEL", subc="OPTIONS",  ktype="float", var="cilevel"),
        Template("HELP", subc="", ktype="bool")])

    global _
    try:
        _("---")
    except:
        def _(msg):
            return msg
    if "HELP" in args:
        helper()
    else:
        processcmd(oobj, args, weightedkappaextension)

def helper():
    """Open html help in default browser window.

    The location is computed from the current module name."""

    import webbrowser, os.path

    path = os.path.splitext(__file__)[0]
    helpspec = "file://" + path + os.path.sep + \
         "STATS_WEIGHTED_KAPPA_SYNTAX_HELP.htm"

    browser = webbrowser.get()
    if not browser.open_new(helpspec):
        print((_("Help file not found:") + helpspec))
try:    
    from extension import helper
except:
    pass

# Add expandvarnames in order to be able to handle TO or ALL specifications

def expandvarnames(varnames):
    """Return varnames with ALL and TO expansion"""
    
    # varnames allows the construct v1, v2, ... ALL to coerce the order
    # as well as TO and ALL expansion
    vardict = None
    varnamesLower = [item.lower() for item in varnames]
    try:
        # check for and process ALL name
        allLoc = varnamesLower.index('all')
    except ValueError:
        allvars = []
    else:
        vardict = spssaux.VariableDict()
        if allLoc != len(varnames) -1:
            raise ValueError(_("""ALL must be the last item in the variable list"""))
        allvars = vardict.expand("ALL")
        varnames = varnames[:-1]

    # process TO
    if 'to' in varnamesLower:
        if not vardict:
            vardict = spssaux.VariableDict()
        varnames = vardict.expand(varnames)
    # append ALL result if it was specified
    # would use set union but order matters
    for item in allvars:
        if not (item in varnames or item.lower() in varnames):
            varnames.append(item)
    return varnames

def weightedkappaextension(variables, wttype=1, cilevel=95):

    varnames = expandvarnames(variables)
    caption = varnames[0] + _(" vs. ") + varnames[1]
    vardict = spssaux.VariableDict(varnames)
    if len(vardict) != len(varnames):
        spss.StartProcedure(_("Weighted Kappa"),"Weighted Kappa")
        table = spss.BasePivotTable("Warnings ","Warnings")
        table.Append(spss.Dimension.Place.row,"rowdim",hideLabels=True)
        rowLabel = CellText.String("1")
        table[(rowLabel,)] = CellText.String(_("""An invalid variable has been specified. This command is not executed."""))
        spss.EndProcedure()
    elif len(varnames) != 2:
        spss.StartProcedure(_("Weighted Kappa"),"Weighted Kappa")
        table = spss.BasePivotTable("Warnings ","Warnings")
        table.Append(spss.Dimension.Place.row,"rowdim",hideLabels=True)
        rowLabel = CellText.String("1")
        table[(rowLabel,)] = CellText.String(_("""Exactly two variables must be specified. This command is not executed."""))
        spss.EndProcedure()
    else:
        try:
            warntext = []
            if cilevel < 50:
                warntext.append(_("CILEVEL cannot be less than 50%. It has been set to 50%."))
                cilevel = 50
            if cilevel > 99.999:
                warntext.append(_("CILEVEL cannot be greater than 99.999%. It has been set to 99.999%."))
                cilevel = 99.999
            if cilevel == int(cilevel):
                cilevel = int(cilevel)
            if wttype != 1:
                if wttype != 2:
                    warntext.append(_("WTTYPE must be 1 or 2. It has been set to 1."))
                    wttype = 1
            varlist = varnames[0] + ' ' + varnames[1]
            spss.Submit("PRESERVE.")
            tempdir = tempfile.gettempdir()
            spss.Submit("""CD "%s".""" % tempdir)
            wtvar = spss.GetWeightVar()
            if wtvar != None:
                spss.Submit(r"""
COMPUTE %s=RND(%s).""" % (wtvar, wtvar))
                spss.Submit(r"""
EXECUTE.""")
            maxloops = 2 * spss.GetCaseCount()
            spss.Submit("""SET PRINTBACK=OFF MPRINT=OFF MXLOOPS=%s.""" % maxloops)
            activeds = spss.ActiveDataset()
            if activeds == "*":
                activeds = "D" + str(random.uniform(.1,1))
                spss.Submit("DATASET NAME %s" % activeds)
            tmpvar1 = "V" + str(random.uniform(.1,1))
            tmpvar2 = "V" + str(random.uniform(.1,1))
            tmpvar3 = "V" + str(random.uniform(.1,1))
            tmpvar4 = "V" + str(random.uniform(.1,1))
            tmpvar5 = "V" + str(random.uniform(.1,1))
            tmpvar6 = "V" + str(random.uniform(.1,1))
            tmpdata1 = "D" + str(random.uniform(.1,1))
            tmpdata2 = "D" + str(random.uniform(.1,1))
            omstag1 = "T" + str(random.uniform(.1,1))
            omstag2 = "T" + str(random.uniform(.1,1))
            omstag3 = "T" + str(random.uniform(.1,1))
            omstag4 = "T" + str(random.uniform(.1,1))
            omstag5 = "T" + str(random.uniform(.1,1))
            omstag6 = "T" + str(random.uniform(.1,1))
            tmpfile1 = "F" + str(random.uniform(.1,1))
            tmpfile2 = "F" + str(random.uniform(.1,1))
            lowlabel = _("""Lower %s%% Asymptotic CI Bound""") % cilevel
            upplabel = _("""Upper %s%% Asymptotic CI Bound""") % cilevel            
            spss.Submit(r"""
DATASET COPY %s WINDOW=HIDDEN.""" % tmpdata1)
            spss.Submit(r"""
DATASET ACTIVATE %s WINDOW=ASIS.""" % tmpdata1)
            filt = spssaux.GetSHOW("FILTER", olang="english")
            if filt != "No case filter is in effect":
                filtcond = filt.strip("(FILTER)")
                select = "SELECT IF " + str(filtcond) + "."
                spss.Submit("""%s""" % select)
                spss.Submit("""EXECUTE.""")
                spss.Submit("""USE ALL.""")
            banana = spssaux.getDatasetInfo(Info="SplitFile")
            if banana != "":
                warntext.append(_("This procedure ignores split file status."))
                spss.Submit(r"""SPLIT FILE OFF.""")
            spss.Submit(r"""
COUNT %s=%s (MISSING).""" % (tmpvar1, varlist))
            spss.Submit(r"""
SELECT IF %s=0.""" % tmpvar1)
            spss.Submit(r"""
EXECUTE.""")
            validn = spss.GetCaseCount()
            if validn < 2:
                spss.Submit(r"""
OMS
 /SELECT TABLES
 /IF COMMANDS=['Weighted Kappa'] SUBTYPES=['Notes']
 /DESTINATION VIEWER=NO
 /TAG = '"%s"'.""" % omstag1)
                spss.StartProcedure(_("Weighted Kappa"),"Weighted Kappa")
                table = spss.BasePivotTable("Warnings ","Warnings")
                table.Append(spss.Dimension.Place.row,"rowdim",hideLabels=True)
                rowLabel = CellText.String("1")
                table[(rowLabel,)] = CellText.String(_("""There are too few complete cases. This command is not executed."""))
                spss.EndProcedure()
                spss.Submit(r"""
OMSEND TAG = ['"%s"'].""" % omstag1)
            else:
                spss.Submit(r"""
AGGREGATE
   /OUTFILE=* MODE=ADDVARIABLES
   /%s=SD(%s)
   /%s=SD(%s).""" % (tmpvar2, varnames[0], tmpvar3, varnames[1]))
                try:
                    cur = spss.Cursor(isBinary=False)
                except:
                    cur = spss.Cursor()
                datarow = cur.fetchone()
                cur.close()
                sd1 = datarow[-2]
                sd2 = datarow[-1]
                if min(sd1,sd2) == 0:
                    spss.Submit(r"""
OMS
 /SELECT TABLES
 /IF COMMANDS=['Weighted Kappa'] SUBTYPES=['Notes']
 /DESTINATION VIEWER=NO
 /TAG = '"%s"'.""" % omstag1)
                    spss.StartProcedure(_("Weighted Kappa"),"Weighted Kappa")
                    table = spss.BasePivotTable("Warnings ","Warnings")
                    table.Append(spss.Dimension.Place.row,"rowdim",hideLabels=True)
                    rowLabel = CellText.String("1")
                    table[(rowLabel,)] = CellText.String(_("""All ratings are the same for at least one rater. This command is not executed."""))
                    spss.EndProcedure()
                    spss.Submit(r"""
OMSEND TAG = ['"%s"'].""" % omstag1)
                else:
                    if len(warntext) > 0:
                        spss.Submit(r"""
OMS
 /SELECT TABLES
 /IF COMMANDS=['Weighted Kappa'] SUBTYPES=['Notes']
 /DESTINATION VIEWER=NO
 /TAG = '"%s"'.""" % omstag1)
                        if len(warntext) == 1:
                            spss.StartProcedure(_("Weighted Kappa"),"Weighted Kappa")
                            table = spss.BasePivotTable("Warnings ","Warnings")
                            table.Append(spss.Dimension.Place.row,"rowdim",hideLabels=True)
                            rowLabel = CellText.String("1")
                            table[(rowLabel,)] = CellText.String("%s" % warntext[0])
                            spss.EndProcedure()
                        if len(warntext) == 2:
                            spss.StartProcedure(_("Weighted Kappa"),"Weighted Kappa")
                            table = spss.BasePivotTable("Warnings ","Warnings")
                            table.Append(spss.Dimension.Place.row,"rowdim",hideLabels=True)
                            rowLabel = CellText.String("1")
                            table[(rowLabel,)] = CellText.String("%s \n" "%s" % (warntext[0], warntext[1]))
                            spss.EndProcedure()
                        if len(warntext) == 3:
                            spss.StartProcedure(_("Weighted Kappa"),"Weighted Kappa")
                            table = spss.BasePivotTable("Warnings ","Warnings")
                            table.Append(spss.Dimension.Place.row,"rowdim",hideLabels=True)
                            rowLabel = CellText.String("1")
                            table[(rowLabel,)] = CellText.String("%s \n" "%s \n" "%s" % (warntext[0], warntext[1], warntext[2]))
                            spss.EndProcedure()                        
                        spss.Submit(r"""
OMSEND TAG = ['"%s"'].""" % omstag1)
                    spss.Submit(r"""
DELETE VARIABLES %s %s.""" % (tmpvar2, tmpvar3))
                    spss.Submit(r"""
AGGREGATE
  /OUTFILE=%s
  /BREAK=%s
  /%s=N.""" % (tmpfile1, varlist, tmpvar4))
                    spss.Submit(r"""
OMS /SELECT ALL EXCEPT=WARNINGS 
 /IF COMMANDS=['Variables to Cases'] 
 /DESTINATION VIEWER=NO
 /TAG = '"%s"'.""" % omstag2)
                    spss.Submit(r"""
VARSTOCASES
  /MAKE %s FROM %s.""" % (tmpvar5, varlist))
                    spss.Submit(r"""
OMSEND TAG = ['"%s"'].""" % omstag2)
                    catdata = []
                    try:
                        cur = spss.Cursor(isBinary=False)
                    except:
                        cur = spss.Cursor()
                    while True:
                        datarow = cur.fetchone()
                        if datarow is None:
                            break
                        catdata.append(datarow[-1])
                    cur.close()
                    cats = list(set(catdata))
                    cattest = 0
                    if any(item != round(item) for item in cats):
                        cattest = 1
                        spss.Submit(r"""
OMS
 /SELECT TABLES
 /IF COMMANDS=['Weighted Kappa'] SUBTYPES=['Notes']
 /DESTINATION VIEWER=NO
 /TAG = '"%s"'.""" % omstag1)
                        spss.StartProcedure(_("Weighted Kappa"),"Weighted Kappa")
                        table = spss.BasePivotTable("Warnings ","Warnings")
                        table.Append(spss.Dimension.Place.row,"rowdim",hideLabels=True)
                        rowLabel = CellText.String("1")
                        table[(rowLabel,)] = CellText.String(_("""Some ratings are not integers. This command is not executed."""))
                        spss.EndProcedure()
                        spss.Submit(r"""
OMSEND TAG = ['"%s"'].""" % omstag1)
                    elif min(cats) < 1.0:
                        spss.Submit(r"""
OMS
 /SELECT TABLES
 /IF COMMANDS=['Weighted Kappa'] SUBTYPES=['Notes']
 /DESTINATION VIEWER=NO
 /TAG = '"%s"'.""" % omstag1)
                        spss.StartProcedure(_("Weighted Kappa"),"Weighted Kappa")
                        table = spss.BasePivotTable("Warnings ","Warnings")
                        table.Append(spss.Dimension.Place.row,"rowdim",hideLabels=True)
                        rowLabel = CellText.String("1")
                        table[(rowLabel,)] = CellText.String(_("""Some ratings are less than 1. This command is not executed."""))
                        spss.EndProcedure()
                        spss.Submit(r"""
OMSEND TAG = ['"%s"'].""" % omstag1)
                    else:
                        spss.Submit(r"""
AGGREGATE
  /OUTFILE=%s
  /BREAK=%s
  /%s=N.""" % (tmpfile2, tmpvar5, tmpvar6))
                        spss.Submit(r"""
DATASET DECLARE %s WINDOW=HIDDEN""" % tmpdata2)
                        spss.Submit(r"""
OMS /SELECT ALL EXCEPT=WARNINGS 
 /IF COMMANDS=['Matrix'] 
 /DESTINATION VIEWER=NO
 /TAG='"%s"'.""" % omstag3)
                        spss.Submit(r"""
MATRIX.
GET x 
  /FILE=%s
  /VARIABLES=%s %s.
GET ratecats
  /FILE=%s
  /VARIABLES=%s.
COMPUTE size=MMAX(ratecats).
COMPUTE y=MAKE(size,size,0).
LOOP i=1 to NROW(y).
+ LOOP j=1 to NCOL(y).
+   LOOP k=1 to NROW(x).
+     DO IF (x(k,1)=i and x(k,2)=j).
+       COMPUTE y(i,j)=x(k,3).
+     END IF.
+   END LOOP.
+ END LOOP.
END LOOP.
COMPUTE wttype=%s.
COMPUTE wt=MAKE(NROW(y),NCOL(y),0).
LOOP i=1 to NROW(y).
+ LOOP j=1 to NCOL(y).
+   DO IF wttype=1.
+     COMPUTE wt(i,j)=1-(ABS(i-j)/(size-1)).
+   ELSE IF wttype=2.
+     COMPUTE wt(i,j)=1-((i-j)/(NROW(y)-1))**2.
+   END IF.
+ END LOOP.
END LOOP.
COMPUTE n=MSUM(y).
COMPUTE prop=y/n.
COMPUTE p_i=RSUM(prop).
COMPUTE p_j=CSUM(prop).
COMPUTE w_i=(wt*T(p_j))*MAKE(1,size,1).
COMPUTE w_j=MAKE(size,1,1)*(T(p_i)*wt).
COMPUTE po=MSUM(wt&*prop).
COMPUTE pe=MSUM(MDIAG(p_i)*wt*MDIAG(p_j)).
COMPUTE kstat=(po-pe)/(1-pe).
COMPUTE var0=(T(p_i)*((wt-(w_i+w_j))&**2)*T(p_j)-pe**2)/(n*(1-pe)**2).
DO IF var0>=0.
+ COMPUTE ase0=SQRT(var0).
ELSE.
+ COMPUTE ase0=-1.
END IF.
DO IF ase0>0.
+ COMPUTE z=kstat/ase0.
+ COMPUTE sig=1-CHICDF(z**2,1).
ELSE.
+ COMPUTE z=-1.
+ COMPUTE sig=-1.
END IF.
COMPUTE var1=(MSUM((prop&*((wt-(w_i+w_j)&*(1-kstat))&**2)))-(kstat-pe*(1-kstat))**2)/(n*(1-pe)**2).
DO IF var1>=0.
+ COMPUTE ase1=SQRT(var1).
ELSE.
+ COMPUTE ase1=-1.
END IF.
SAVE {wttype,kstat,ase1,z,sig,ase0}
   /OUTFILE=%s
   /VARIABLES=wttype,kstat,ase1,z,sig,ase0.
END MATRIX.""" % (tmpfile1, varlist, tmpvar4, tmpfile2, tmpvar5, wttype, tmpdata2))
                        spss.Submit(r"""
OMSEND TAG=['"%s"'].""" % omstag3)
                        spss.Submit(r"""
DATASET ACTIVATE %s WINDOW=ASIS.""" % tmpdata2)
                        spss.Submit(r"""
DO IF ase0=-1.
+ RECODE z sig (-1=SYSMIS).
END IF.
EXECUTE.
DELETE VARIABLES ase0.
RECODE ase1 (-1=SYSMIS).
COMPUTE lower=kstat-SQRT(IDF.CHISQUARE(%s/100,1))*ase1.""" % cilevel)
                        spss.Submit(r"""
COMPUTE upper=kstat+SQRT(IDF.CHISQUARE(%s/100,1))*ase1.""" % cilevel)
                        spss.Submit(r"""
FORMATS kstat ase1 z sig lower upper (F11.3).
VARIABLE LABELS kstat %s.""" % _smartquote(_("""Kappa""")))
                        spss.Submit(r"""
VARIABLE LABELS ase1 %s.""" % _smartquote(_("""Asymptotic Standard Error""")))
                        spss.Submit(r"""
VARIABLE LABELS z %s.""" % _smartquote(_("""Z""")))
                        spss.Submit(r"""
VARIABLE LABELS sig %s. """ % _smartquote(_("""P Value""")))
                        spss.Submit(r"""
VARIABLE LABELS lower %s. """ % _smartquote(_(lowlabel)))
                        spss.Submit(r"""
VARIABLE LABELS upper %s. """ % _smartquote(_(upplabel)))
                        if wttype == 1:
                            spss.Submit(r"""
VARIABLE LABELS wttype %s.""" % _smartquote(_("""Linear""")))
                        if wttype == 2:
                            spss.Submit(r"""
VARIABLE LABELS wttype %s.""" % _smartquote(_("""Quadratic""")))
                        spss.Submit(r"""
EXECUTE.
""")
                        spss.Submit(r"""
OMS
  /SELECT TABLES 
  /IF COMMANDS=['Weighted Kappa'] SUBTYPES=['Notes']
  /DESTINATION VIEWER=NO
  /TAG = '"%s"'.""" % omstag4)
                        spss.Submit(r"""
OMS
  /SELECT TEXTS
  /IF COMMANDS=['Weighted Kappa'] LABELS=['Active Dataset']
  /DESTINATION VIEWER=NO
  /TAG = '"%s"'.""" % omstag5)
                        if len(warntext) > 0:
                            spss.Submit(r"""
OMS
 /SELECT HEADINGS
 /IF COMMANDS=['Weighted Kappa']
 /DESTINATION VIEWER=NO
 /TAG = '"%s"'.""" % omstag6)
                        try:
                            cur = spss.Cursor(isBinary=False)
                        except:
                            cur = spss.Cursor()
                        data=cur.fetchone()
                        cur.close()
                        spss.StartProcedure(_("Weighted Kappa"),"Weighted Kappa")
                        table = spss.BasePivotTable(_("Weighted Kappa"),"Kappa",caption=caption)
                        table.SimplePivotTable(rowdim = _("Weighting"),
                           rowlabels = [CellText.String(spss.GetVariableLabel(0))],
                           coldim = "",
                           collabels = [spss.GetVariableLabel(1),spss.GetVariableLabel(2),spss.GetVariableLabel(3),spss.GetVariableLabel(4), \
                                             spss.GetVariableLabel(5),spss.GetVariableLabel(6)],
                           cells = [data[1],data[2],data[3],data[4],data[5],data[6]])
                        spss.EndProcedure()
                        if len(warntext) > 0:
                            spss.Submit(r"""
OMSEND TAG = ['"%s"'].""" % omstag6)
        finally:
            try:
                spss.Submit(r"""
DATASET CLOSE %s.""" % tmpdata1)
                spss.Submit(r"""
DATASET ACTIVATE %s WINDOW=ASIS.""" % activeds)
                if validn >= 2:
                    if min(sd1,sd2) > 0:
                        if cattest == 0:
                            if min(cats) >= 1:
                                spss.Submit(r"""
OMSEND TAG=['"%s"' '"%s"'].""" % (omstag4,omstag5))                
                                spss.Submit(r"""
DATASET CLOSE %s.""" % tmpdata2)
                                spss.Submit(r"""
ERASE FILE=%s.""" % tmpfile2)
                        spss.Submit(r"""
ERASE FILE=%s.""" % tmpfile1)
            except:
                pass
            spss.Submit(r"""
RESTORE.
""")

