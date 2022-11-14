import cs112_f22_week8_linter
from cmu_112_graphics import *
from imageManager import *

def drawSelector(app, canvas):
    if app.selectorMode == "Fight":
        canvas.create_image(375, 375, image=
    ImageTk.PhotoImage(app.img["MenuFight"])
    )
    elif app.selectorMode == "Pokemon":
        canvas.create_image(375, 375, image=
    ImageTk.PhotoImage(app.img["MenuPokemon"])
    )
    elif app.selectorMode == "Bag":
        canvas.create_image(375, 375, image=
    ImageTk.PhotoImage(app.img["MenuBag"])
    )
    elif app.selectorMode == "Run":
        canvas.create_image(375, 375, image=
    ImageTk.PhotoImage(app.img["MenuRun"])
    )

def manageSelector(app, next):
    finalChange = app.selectorMode
    if app.selectorMode == "Fight":
        if next == "down":
            finalChange = "Pokemon"
        elif next == "right":
            finalChange = "Bag"
    elif app.selectorMode == "Bag":
        if next == "down":
            finalChange = "Run"
        elif next == "left":
            finalChange = "Fight"
    elif app.selectorMode == "Pokemon":
        if next == "up":
            finalChange = "Fight"
        elif next == "right":
            finalChange = "Run"
    elif app.selectorMode == "Run":
        if next == "up":
            finalChange = "Bag"
        elif next == "left":
            finalChange = "Pokemon"
    app.selectorMode = finalChange

def chooseOption(app):
    if app.selectorMode == "Fight":
        app.mode = "moveSelect"
    elif app.selectorMode == "Bag":
        app.mode = "bagSelect"
    elif app.selectorMode == "Pokemon":
        app.mode = "pokemonSelect"
    elif app.selectorMode == "Run":
        app.mode = "run"

def drawTextbox(app, canvas):
    canvas.create_image(250, 375, image=
    ImageTk.PhotoImage(app.img["TextBackground"])
    )
    if app.mainBattleUI_txtDone == False:
        addOn = "\n..."
        textWidth = 440
    else:
        addOn = ""
        textWidth = 200
    canvas.create_text(29, 339,
                    text=app.mainBattleUI_txt + addOn, 
                    fill='gray',
                    font=app.GeneralFont,
                    anchor="nw",
                    width=textWidth)
    canvas.create_text(30, 340,
                    text=app.mainBattleUI_txt + addOn, 
                    fill='white',
                    font=app.GeneralFont,
                    anchor="nw",
                    width=textWidth)

def drawBackground(app, canvas):
    canvas.create_image(250, 150, image=
    ImageTk.PhotoImage(app.img[app.battleBackgroundSelection])
    )

def selectorActive(app):
    app.mainBattleUI_txtDone = True

def mainBattleUI_keyPressed(app, event):
    if app.mainBattleUI_txtDone == True:
        if (event.key == "Up"):
            manageSelector(app, "up")
        if (event.key == "Down"):
            manageSelector(app, "down")
        if (event.key == "Left"):
            manageSelector(app, "left")
        if (event.key == "Right"):
            manageSelector(app, "right")
        if (event.key == "Enter"):
            chooseOption(app)
    else:
        if (event.key == "Enter"):
            selectorActive(app)
      
def mainBattleUI_redrawAll(app, canvas):
    drawBackground(app, canvas)
    drawTextbox(app, canvas)
    if app.mainBattleUI_txtDone == True:
        drawSelector(app, canvas)
    
