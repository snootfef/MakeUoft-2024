from recog import HandRecog as hd
import time

HD = hd()
history = []
directionHistory = [""] * 20
while True:
    hand = HD.getHand()
    if hand == []:
        continue
    if len(history) == 4:
        history.pop(0)
    history.append(hand)
    directionHistory.pop(0)
    if HD.handIsOpen(hand) and HD.handUp(hand):
      if len(history) == 4:
          handDirection = HD.handMovingDirection(history)
          directionHistory.append(handDirection)
          if HD.isWaving(directionHistory):
              print("Waving")
    time.sleep(0.05)
    