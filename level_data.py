from actor import Enemy


enemyImage = ["images/enemy1.png", "images/enemy2.png", "images/enemy3.png"]
# cols, rows, startX, startY, distX, distY, speedX, speedY, index for enemyImage
data       = [[8, 4, 20, -60, 70, 70, 2, 40, 1],
              [6, 4, 20, -60, 90, 70, 3, 30, 2],
              [6, 3, 20, 20, 90, 90, 4, 50, 0],
              [5, 4, 20, 20, 100, 80, 5, 60, 1]]

#spawn enemies with different properties
def spawn_enemies(screen, level):
    enemies = []
    rec     = data[level]
    pic     = enemyImage[rec[-1]]
    for i in range(rec[0]):
        for j in range(rec[1]):
            enemy = Enemy(pic, screen, rec[2]+i*rec[4], rec[3]+j*rec[5], changeX=rec[6], changeY=rec[7])
            enemies.append(enemy)

    total = rec[0] * rec[1]

    return [enemies, total]





