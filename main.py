import pygame
from pygame.locals import *
pygame.init()

_evt_names = {
  QUIT            :"quit",# none
  ACTIVEEVENT     :"actionevent",# gain, state
  KEYDOWN         :"keydown",# unicode, key, mod
  KEYUP           :"keyup",# key, mod
  MOUSEMOTION     :"mousemotion",# pos, rel, buttons
  MOUSEBUTTONUP   :"mousebuttonup",# pos, button
  MOUSEBUTTONDOWN :"mousebuttondown",# pos, button
  JOYAXISMOTION   :"joyaxismotion",# joy, axis, value
  JOYBALLMOTION   :"joyballmotion",# joy, ball, rel
  JOYHATMOTION    :"joyhaltmotion",# joy, hat, value
  JOYBUTTONUP     :"joybuttonup",# joy, button
  JOYBUTTONDOWN   :"joybuttondown",# joy, button
  VIDEORESIZE     :"videoresize",# size, w, h
  VIDEOEXPOSE     :"videoexpose",# none
  USEREVENT       :"userevent"
}
    
class PygameApp(object):
  def __init__(self, mode=(640,480), fps=60):
    pygame.init()
    self.running = False
    self.mode = mode
    self.fps = fps

  def run(self):
    self.running = True
    clock = pygame.time.Clock()
    self.window = pygame.display.set_mode(self.mode)
    #Start
    getattr(self, "on_start", lambda :None)()
    #Body
    while self.running:
      for evt in pygame.event.get():
        getattr(self, "on_%s" % _evt_names[evt.type], lambda *a:None)(evt)
      dt = clock.tick(self.fps)
      self.on_frame(dt)
    #Finish
    getattr(self, "on_finish", lambda :None)()
      
  def on_quit(self, evt):
    self.running = False

class DirtyRectangleMixin(object):
  def __init__(self, *a, **b):
    self._dirty_rects = []

  def mark_dirty(self, rect):
    self._dirty_rects.append(rect)

  def update_dirty(self):
    pygame.display.update(self._dirty_rects)
    self._dirty_rects = [] 
 
class ExamplePygameApp(DirtyRectangleMixin, PygameApp):
  def __init__(self):
    DirtyRectangleMixin.__init__(self)
    PygameApp.__init__(self, fps=1000)
    self.history = [0]*1000
    self.append_pos = 0

    self.font = pygame.font.Font(None, 30)

  def append_dt(self, dt):
    self.history[self.append_pos] = dt
    self.append_pos += 1
    self.append_pos %= len(self.history)

  def on_start(self):
    self.window.fill((255,255,255))
#    pygame.display.flip()

  def on_frame(self, dt):
    if not dt: return
    self.append_dt(dt)
    fps = 1000/(sum(self.history)/float(len(self.history)))

    
    rendered_text = self.font.render("fps: %s" % fps, 0, (255,0,0))
    rect = rendered_text.get_rect()
    rect.topleft = (200,200)
   
    pygame.draw.rect(self.window, (255,255,255), rect) 
    self.window.blit(rendered_text, rect)

    #pygame.display.flip()
    self.mark_dirty(rect)
    self.update_dirty()
if __name__ == "__main__":
  app = ExamplePygameApp()
  app.run()
  
