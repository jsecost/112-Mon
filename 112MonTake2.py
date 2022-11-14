
import cs112_f22_week8_linter
from cmu_112_graphics import *
from mainBattleUI import *
from battleDrawBothPokemon import *
from newBattle import *
from mainBattleUI import *
from imageManager import *

import decimal
import copy

def appStarted(app):

    ##  Window Size / Params / Settings ##

    app.size = (500, 450)
    app.width = 500
    app.height = 450
    app.GeneralFont = "Helvetica 16"

    ##  Starting Mode   ##
    app.mainBattleUI_txtDone = False
    app.battleBackgroundSelection = "battleBackgroundCut"
    app.mainBattleUI_txt = "Battle Started"
    app.selectorMode = "Fight"
    app.mode = "mainBattleUI"
    

    ##  Load Images ##
    app.assetsFolderPath = "assets/"
    loadAssets(app)

runApp(width=500, height=450)




