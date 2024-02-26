def loadWinConditions(var,config):
        var.winMessage = config.get("Meta", "winMessage")
        var.looseMessage = config.get("Meta", "looseMessage")
        
        if config.get("Meta", "winByEliminatingEnemy") == "0":
            var.winByEliminatingEnemy = False
        else:
            var.winByEliminatingEnemy = True


        if config.get("Meta", "looseByEliminatingEnemy") == "0":
            var.looseByEliminatingEnemy = False
        else:
            var.looseByEliminatingEnemy = True

        if config.get("Meta", "winByEliminatingPlayer") == "0":
            var.winByEliminatingPlayer = False
        else:
            var.winByEliminatingPlayer = True

        if config.get("Meta", "looseByEliminatingPlayer") == "0":
            var.looseByEliminatingPlayer = False
        else:
            var.looseByEliminatingPlayer = True

        if config.get("Meta", "winByDisablingEnemy") == "0":
            var.winByDisablingEnemy = False
        else:
            var.winByDisablingEnemy = True

        if config.get("Meta", "winByDisablingPlayer") == "0":
            var.winByDisablingPlayer = False
        else:
            var.winByDisablingPlayer = True

        if config.get("Meta", "looseByDisablingPlayer") == "0":
            var.looseByDisablingPlayer = False
        else:
            var.looseByDisablingPlayer = True

        if config.get("Meta", "looseByDisablingEnemy") == "0":
            var.looseByDisablingEnemy = False
        else:
            var.looseByDisablingEnemy = True

        if config.get("Meta", "winByEliminating0") == "0":
            var.winByEliminating0 = False
        else:
            var.winByEliminating0 = True
        if config.get("Meta", "winByEliminating1") == "0":
            var.winByEliminating1 = False
        else:
            var.winByEliminating1 = True
        if config.get("Meta", "winByEliminating2") == "0":
            var.winByEliminating2 = False
        else:
            var.winByEliminating2 = True
        if config.get("Meta", "winByEliminating3") == "0":
            var.winByEliminating3 = False
        else:
            var.winByEliminating3 = True
        if config.get("Meta", "winByEliminating4") == "0":
            var.winByEliminating4 = False
        else:
            var.winByEliminating4 = True
        if config.get("Meta", "winByEliminating5") == "0":
            var.winByEliminating5 = False
        else:
            var.winByEliminating5 = True
            
        if config.get("Meta", "looseByEliminating0") == "0":
            var.looseByEliminating0 = False
        else:
            var.looseByEliminating0 = True
        if config.get("Meta", "looseByEliminating1") == "0":
            var.looseByEliminating1 = False
        else:
            var.looseByEliminating1 = True
        if config.get("Meta", "looseByEliminating2") == "0":
            var.looseByEliminating2 = False
        else:
            var.looseByEliminating2 = True
        if config.get("Meta", "looseByEliminating3") == "0":
            var.looseByEliminating3 = False
        else:
            var.looseByEliminating3 = True
        if config.get("Meta", "looseByEliminating4") == "0":
            var.looseByEliminating4 = False
        else:
            var.looseByEliminating4 = True
        if config.get("Meta", "looseByEliminating5") == "0":
            var.looseByEliminating5 = False
        else:
            var.looseByEliminating5 = True

        if config.get("Meta", "looseByDisabling0") == "0":
            var.looseByDisabling0 = False
        else:
            var.looseByDisabling0 = True
        if config.get("Meta", "looseByDisabling1") == "0":
            var.looseByDisabling1 = False
        else:
            var.looseByDisabling1 = True
        if config.get("Meta", "looseByDisabling2") == "0":
            var.looseByDisabling2 = False
        else:
            var.looseByDisabling2 = True
        if config.get("Meta", "looseByDisabling3") == "0":
            var.looseByDisabling3 = False
        else:
            var.looseByDisabling3 = True
        if config.get("Meta", "looseByDisabling4") == "0":
            var.looseByDisabling4 = False
        else:
            var.looseByDisabling4 = True
        if config.get("Meta", "looseByDisabling5") == "0":
            var.looseByDisabling5 = False
        else:
            var.looseByDisabling5 = True

        if config.get("Meta", "winByDisabling0") == "0":
            var.winByDisabling0 = False
        else:
            var.looseByDisabling0 = True
        if config.get("Meta", "winByDisabling1") == "0":
            var.winByDisabling1 = False
        else:
            var.winByDisabling1 = True
        if config.get("Meta", "winByDisabling2") == "0":
            var.winByDisabling2 = False
        else:
            var.winByDisabling2 = True
        if config.get("Meta", "winByDisabling3") == "0":
            var.winByDisabling3 = False
        else:
            var.winByDisabling3 = True
        if config.get("Meta", "winByDisabling4") == "0":
            var.winByDisabling4 = False
        else:
            var.winByDisabling4 = True
        if config.get("Meta", "winByDisabling5") == "0":
            var.winByDisabling5 = False
        else:
            var.winByDisabling5 = True

        if config.has_option('Meta', 'winBySeeingLandmarks'):
            if config.get("Meta", "winBySeeingLandmarks") == "0":
                var.winBySeeingLandmarks = False
            else:
                var.winBySeeingLandmarks = True

        if config.has_option('Meta', 'winByDomination'):
            if config.get("Meta", "winByDomination") == "0":
                var.winByDomination = False
            else:
                var.winByDomination = True
        if config.has_option('Meta', 'looseByDomination'):
            if config.get("Meta", "looseByDomination") == "0":
                var.looseByDomination = False
            else:
                var.looseByDomination = True
                
        if config.has_option('Meta', 'playerRespawns'):
            var.enemyRespawns = int(config.get("Meta", "playerRespawns"))
        if config.has_option('Meta', 'enemyRespawns'):
            var.enemyRespawns = int(config.get("Meta", "enemyRespawns"))

        var.winMessage = config.get("Meta", "winMessage")