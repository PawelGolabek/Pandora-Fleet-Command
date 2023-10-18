
                if(colorWeight < 600 and colorWeight > 400):
                    movementPenality = gameRules.movementPenalityMedium
                elif(colorWeight < 400 and colorWeight > 200):
                    movementPenality = gameRules.movementPenalityMedium
                    currentOrderValue -= 400
                elif(colorWeight <= 200):
                    movementPenality = gameRules.movementPenalityHard
                    currentOrderValue -= 4000
                else:
                    movementPenality = 0.000001  # change