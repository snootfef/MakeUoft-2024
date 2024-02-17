from recog import HandRecog as hd
import time

HD = hd()
history = []
directionHistory = [["", False]] * 20
count = 0
buffer = time.time()
waving = False

while True:
    hand = HD.getHand()
    if hand == []:
        continue
    if len(history) == 4:
        history.pop(0)
    history.append(hand)
    if len(directionHistory) == 20:
      directionHistory.pop(0)
    if HD.handIsOpen(hand) and HD.handUp(hand):
      if len(history) == 4:
          handDirection = HD.handMovingDirection(history)
          directionHistory.append(handDirection)
          waved = HD.isWaving(directionHistory)
          bufferTime = time.time() - buffer
          if waved and not waving and bufferTime > 1:
              print("Waving " + str(count))
              count += 1
              buffer = time.time()
              waving = True
          elif not waved and waving and bufferTime > 3:
              print("Stopped Waving")
              buffer = time.time()
              waving = False
    else:
      directionHistory.append(["", False])
      if waving:
        print("Stopped Waving")
        waving = False
        buffer = time.time()
    time.sleep(0.05)
    