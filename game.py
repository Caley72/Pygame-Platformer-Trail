import pygame
from pygame.locals import*

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 800
screen_height = 800
screen =pygame.display.set_mode((screen_width, screen_height))

#Define Game Variables
tile_size = 40

#Load Images
luminous_object = pygame.image.load('Images/sprites/Environment/Red_Moon.png')
bg_img = pygame.image.load('Images/sprites/Environment/Sky.png')

def draw_grid():
    for line in range (0, 20):
        pygame.draw.line(screen,(255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen,(255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))

class Player1():
    def __init__(self, x, y):
        self.images_static = [] #For Right
        self.images_right = []
        self.images_left = []
        self.jump_right = []
        self.index = 0
        self.counter = 0    

        # Load static images (idle)
        for num in range(1, 5):
            static_right = pygame.image.load(f'Images/sprites/Characters/Black_Static{num}.png')
            static_right = pygame.transform.scale(static_right, (60, 80))
            self.images_static.append(static_right)
        
        # Load running images (right)
        for num in range(1, 6):            
            run_right = pygame.image.load(f'Images/sprites/Characters/Black_Run{num}.png')
            run_right = pygame.transform.scale(run_right, (60, 80))
            self.images_right.append(run_right)

        #Load Jump Image
        jump = pygame.image.load('Images/sprites/Characters/Black_Jump.png')
        jump = pygame.transform.scale(jump, (40, 80))
        self.jump_right.append(jump)

        # Flip the running images for the left direction
        self.images_left = [pygame.transform.flip(img, True, False) for img in self.images_right]
        #Flip the Static image for the left direction
        self.static_left = [pygame.transform.flip(img, True, False) for img in self.images_static]
        #Flip Jump to left direction
        self.jump_left = [pygame.transform.flip(img, True, False) for img in self.jump_right]

        # The default image is the first static image
        self.image = self.images_static[self.index]  # Default for Static Image
        self.image_move = self.images_right[self.index]  # Default to first running image
        self.jump = self.jump_right[self.index]
        self.rect = self.image.get_rect()
        self.rect = self.image_move.get_rect()
        self.rect = self.jump.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0

    def update(self):
        dx = 0
        dy = 0
        animation_cooldown = 0.5  # The cooldown for the animation
        key = pygame.key.get_pressed()  # Get keypress
        
        # Jumping
        if key[pygame.K_UP] and not self.jumped:
            self.vel_y = -14
            self.jumped = True

        if not key[pygame.K_UP]:
            self.jumped = False

        # Dash Down
        if key[pygame.K_DOWN]:
            dy += 50
        
        # Left movement
        if key[pygame.K_LEFT]:
            dx -= 10
            # Flip both the static image and the running animation for left movement
            self.image_move = self.images_left[self.index]
            self.image = self.static_left[self.index]  # Flip the static image for left
            self.direction = -1

        # Right movement
        if key[pygame.K_RIGHT]:
            dx += 10
            # Reset to the original (non-flipped) static and running images for right movement
            self.image_move = self.images_right[self.index]
            self.image = self.images_static[self.index]  # Reset static image to default (non-flipped)
            self.direction = 1

        # Handle Animations
        self.counter += 1
        if self.counter > animation_cooldown:
            self.counter = 0
            self.index += 1
            
            # Loop through images
            if self.index >= len(self.images_static):
                self.index = 0
            if dx == 0:
                # Player is idle (no movement), show static image
                self.black_create = self.images_static[self.index]
                if self.direction == 1:
                    # Player is idle (no movement), show static image
                    self.black_create = self.images_static[self.index]   
                else:
                    self.black_create = self.static_left[self.index]        
            else:
                # Player is moving (left or right), show running animation
                self.black_create = self.images_right[self.index] if dx > 0 else self.images_left[self.index]
        # Add gravity
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        #Add Collision
        for tile in world.tile_list:
            #Check for collision in x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            #Check for collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #check below the ground i.e jumping
                if self.vel_y < 0 :
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                #check above the ground i.e falling
                elif self.vel_y >= 0 :
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0

        # Update Player Coordinates
        self.rect.x += dx
        self.rect.y += dy

        # Check if player is on the ground
        if self.rect.bottom > screen_height - 80:
            self.rect.bottom = screen_height - 80
            dy = 0

        # Draw the player on the screen
        screen.blit(self.black_create, self.rect)
        pygame.draw.rect(screen, (255, 255, 255, 100), self.rect, 2)

class World(): 
    def __init__(self, data):
        self.tile_list = []
        #load images for Background
        wall = pygame.image.load('Images/sprites/Environment/Dirt_Wall.png')
        floor = pygame.image.load('Images/sprites/Environment/Dirt_Floor.png')
        floorEdgeLeft = pygame.image.load('Images/sprites/Environment/Dirt_Edge_Floor_Left.png')
        floorEdgeRight = pygame.image.load('Images/sprites/Environment/Dirt_Edge_Floor_Right.png')
        wallEdgeLeft = pygame.image.load('Images/sprites/Environment/Dirt_Edge_Left.png')
        wallEdgeRight = pygame.image.load('Images/sprites/Environment/Dirt_Edge_Right.png')
        gateInside = pygame.image.load('Images/sprites/Environment/Gate_Inside.png')
        gateSide = pygame.image.load('Images/sprites/Environment/Gate_Side.png')
        gateTop = pygame.image.load('Images/sprites/Environment/Gate_Top.png')
        gateEdge = pygame.image.load('Images/sprites/Environment/Gate_Edge.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(wall, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(floor, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    img = pygame.transform.scale(floorEdgeLeft, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 4:
                    img = pygame.transform.scale(floorEdgeRight, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 5:
                    img = pygame.transform.scale(wallEdgeLeft, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 6:
                    img = pygame.transform.scale(wallEdgeRight, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 7:
                    img = pygame.transform.scale(gateInside, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 8:
                    img = pygame.transform.scale(gateSide, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 9:
                    img = pygame.transform.scale(gateTop, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 10:
                    img = pygame.transform.scale(gateEdge, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 0), tile[1], 2)

world_data =[
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 9, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 9, 1],
[1, 7, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 7, 1],
[1, 7, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 7, 1],
[1, 2, 2, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 2, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 3, 2, 2, 2, 2, 2, 2, 2, 2, 4, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 5, 1, 1, 1, 1, 1, 1, 6, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

#Players Position
player1 =Player1(240, screen_height - 400)

world = World(world_data)

run = True
while run:

    clock.tick(fps)

    #Images to Screen
    screen.fill((20, 250, 150))
    screen.blit(bg_img, (0,0))
    screen.blit(luminous_object, (100,100))


    world.draw()
    player1.update()
    draw_grid()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
pygame.quit()