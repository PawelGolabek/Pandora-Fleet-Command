def loadWinConditions(var,config):
        var.winMessage = config.get("Meta", "winMessage")
        var.looseMessage = config.get("Meta", "looseMessage")
        
        var.looseByEliminatingEnemy = config.get("Meta", "looseByEliminatingEnemy", fallback = "0") == "1"
        var.looseByEliminatingPlayer = config.get("Meta", "looseByEliminatingPlayer", fallback = "0") == "1"
        var.winByEliminatingEnemy = config.get("Meta", "winByEliminatingEnemy", fallback = "0") == "1"
        var.winByEliminatingPlayer = config.get("Meta", "winByEliminatingPlayer", fallback = "0") == "1"
        var.winByDisablingEnemy = config.get("Meta", "winByDisablingEnemy", fallback = "0") == "1"
        var.winByDisablingPlayer = config.get("Meta", "winByDisablingPlayer", fallback = "0") == "1"
        var.looseByDisablingPlayer = config.get("Meta", "looseByDisablingPlayer", fallback = "0") == "1"
        var.looseByDisablingEnemy = config.get("Meta", "looseByDisablingEnemy", fallback = "0") == "1"

        var.winByEliminating0 = config.get("Meta", "winByEliminating0", fallback = "0") == "1"
        var.winByEliminating1 = config.get("Meta", "winByEliminating1", fallback = "0") == "1"
        var.winByEliminating2 = config.get("Meta", "winByEliminating2", fallback = "0") == "1"
        var.winByEliminating3 = config.get("Meta", "winByEliminating3", fallback = "0") == "1"
        var.winByEliminating4 = config.get("Meta", "winByEliminating4", fallback = "0") == "1"
        var.winByEliminating5 = config.get("Meta", "winByEliminating5", fallback = "0") == "1"

        var.looseByEliminating0 = config.get("Meta", "looseByEliminating0", fallback = "0") == "1"
        var.looseByEliminating1 = config.get("Meta", "looseByEliminating1", fallback = "0") == "1"
        var.looseByEliminating2 = config.get("Meta", "looseByEliminating2", fallback = "0") == "1"
        var.looseByEliminating3 = config.get("Meta", "looseByEliminating3", fallback = "0") == "1"
        var.looseByEliminating4 = config.get("Meta", "looseByEliminating4", fallback = "0") == "1"
        var.looseByEliminating5 = config.get("Meta", "looseByEliminating5", fallback = "0") == "1"

        var.looseByDisabling0 = config.get("Meta", "looseByDisabling0", fallback = "0") == "1"
        var.looseByDisabling1 = config.get("Meta", "looseByDisabling1", fallback = "0") == "1"
        var.looseByDisabling2 = config.get("Meta", "looseByDisabling2", fallback = "0") == "1"
        var.looseByDisabling3 = config.get("Meta", "looseByDisabling3", fallback = "0") == "1"
        var.looseByDisabling4 = config.get("Meta", "looseByDisabling4", fallback = "0") == "1"
        var.looseByDisabling5 = config.get("Meta", "looseByDisabling5", fallback = "0") == "1"

        var.winByDisabling0 = config.get("Meta", "winByDisabling0", fallback = "0") == "1"
        var.winByDisabling1 = config.get("Meta", "winByDisabling1", fallback = "0") == "1"
        var.winByDisabling2 = config.get("Meta", "winByDisabling2", fallback = "0") == "1"
        var.winByDisabling3 = config.get("Meta", "winByDisabling3", fallback = "0") == "1"
        var.winByDisabling4 = config.get("Meta", "winByDisabling4", fallback = "0") == "1"
        var.winByDisabling5 = config.get("Meta", "winByDisabling5", fallback = "0") == "1"

        if config.has_option('Meta', 'winBySeeingLandmarks'):
            if config.get("Meta", "winBySeeingLandmarks") == "0":
                var.winBySeeingLandmarks = False
            else:
                var.winBySeeingLandmarks = True

        var.winByDomination = config.get("Meta", "winByDomination", fallback="0") == "1"
        var.looseByDomination = config.get("Meta", "looseByDomination", fallback="0") == "1"
                
        if config.has_option('Meta', 'playerRespawns'):
            var.enemyRespawns = int(config.get("Meta", "playerRespawns"))
        if config.has_option('Meta', 'enemyRespawns'):
            var.enemyRespawns = int(config.get("Meta", "enemyRespawns"))

        var.winMessage = config.get("Meta", "winMessage")

        var.respawns = int(config.get("Meta", "respawns", fallback = "0"))
        var.enemyRespawns = int(config.get("Meta", "enemyRespawns", fallback = "0"))