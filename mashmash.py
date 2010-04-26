#!/usr/bin/python
import pygame, sys,os, random, string
from pygame.locals import * 

# figure out the install base to use with image and sound loading
progInstallBase = os.path.dirname(os.path.normpath(sys.argv[0]));


# Load image in data/, handling setting of the transparency color key
def load_image(name, colorkey=None):
    fullname = os.path.join(progInstallBase, 'data', name)
    
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print "Cannot load image:", name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

# Load sound file in data/
def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join(progInstallBase, 'data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print "Cannot load sound:", fullname
        raise SystemExit, message
    return sound

# Loads a list of sounds
def load_sounds(lst):
    result = []
    for name in lst:
        result.append(load_sound(name))
    return result
    
# Processes events
def input(events, quit_pos):
    
    for event in events: 
        if event.type == QUIT: 
            sys.exit(0) 
        elif event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
            #print "eepos: %s" % (quit_pos)
            
            if event.type == KEYDOWN:
                if event.key == K_q:
                    quit_pos = 1
                elif ((event.key == K_u) and (quit_pos == 1)):
                    quit_pos = 2
                elif event.key == K_i and quit_pos == 2:
                    quit_pos = 3
                elif event.key == K_t and quit_pos == 3:
                    sys.exit(0)
                else:
                    quit_pos = 0

            # Clear the background 20% of the time
            if random.randint(0, 20) == 1:
                screen.blit(background, (0, 0))
                pygame.display.flip()
            

            if event.type == MOUSEBUTTONDOWN or not(is_alpha(event.key)):
                print_image()
                
            else:
                try:
                    letters[event.key-97].play()
                except:
                    sounds[random.randint(0, len(sounds) -1)].play()
                print_letter(event.key)
                
            
            pygame.display.flip() 
    return quit_pos

# Prints an image at a random location
def print_image():
    ref = random.randint(0, len(images) -1)
    img = images[ref]
    sounds[ref].play()
    w = random.randint(0, WIDTH-img.get_width())
    h = random.randint(0, HEIGHT-img.get_height())
    screen.blit(img, (w, h)) 

# Is the key that was pressed alphanumeric
def is_alpha(key):
    return key < 255 and (chr(key) in string.letters or chr(key) in string.digits)

# Prints a letter at a random location
def print_letter(key):
    font = pygame.font.Font(None, 256)
    text = font.render(chr(key), 1, colors[random.randint(0, len(colors) -1)])
    textpos = text.get_rect()
    center = (textpos.width / 2, textpos.height / 2)
    w = random.randint(0+center[0], WIDTH-center[0])
    h = random.randint(0+center[1], HEIGHT-center[1])
    textpos.centerx = w
    textpos.centery = h
    screen.blit(text, textpos) 

# Main application
#
if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'
 
pygame.init() 
dimensions = pygame.display.list_modes()[0]
WIDTH = dimensions[0]
HEIGHT = dimensions[1]
window = pygame.display.set_mode(dimensions, pygame.FULLSCREEN) 
pygame.display.set_caption('MashMash') 
screen = pygame.display.get_surface() 

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))

screen.blit(background, (0, 0))
pygame.display.flip()

sounds = load_sounds(('dog.wav',
                        'cat.wav',
                        'hannah.wav',
                        'cat2.wav',
                        'monkey.wav',
                        'cow.wav',
                        'pig.wav',
                        'duck.wav',
                        'sheep.wav',
                        'lion.wav'))
letters = load_sounds(('A.ogg','B.ogg','C.ogg','D.ogg','E.ogg','F.ogg','G.ogg','H.ogg','I.ogg','J.ogg','K.ogg','L.ogg','M.ogg','N.ogg','O.ogg','P.ogg','Q.ogg','R.ogg','S.ogg','T.ogg','U.ogg','V.ogg','W.ogg','X.ogg','Y.ogg','Z.ogg'))
colors = ((0,0,255), (255,0,0), (0,255,0), (255, 0, 255),(255, 255, 0))
images = (load_image('dog.gif')[0],
            load_image('cat.gif')[0],
            load_image('hannah.gif')[0],
            load_image('cat2.gif')[0],
            load_image('monkey.gif')[0],
            load_image('cow.gif')[0],
            load_image('pig.gif')[0],
            load_image('duck.gif')[0],
            load_image('sheep.gif')[0],
            load_image('lion.gif')[0])

quit_pos = 0   

clock = pygame.time.Clock()
while True:
    clock.tick(60)
    quit_pos = input(pygame.event.get(), quit_pos) 

