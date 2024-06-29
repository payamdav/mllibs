class CrossHair:
  def __init__(self, fig) -> None:
    self.lw = 0.5
    self.color = 'w'
    self.alpha = 0.5
    self.horizontal = True
    self.vertical = True
    
    self.fig = fig
    self.fig.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
    self.hls = []
    self.vls = []
  
  def on_mouse_move(self, event):
    if event.inaxes:
      [hl.remove() for hl in self.hls]
      self.hls.clear()
      [vl.remove() for vl in self.vls]
      self.vls.clear()
      for ax in self.fig.axes:
        if ax.get_visible():
          if self.horizontal:
            ylim = ax.get_ylim()
            if ylim[0] < event.ydata < ylim[1]:        
              self.hls.append(ax.axhline(event.ydata, color=self.color, lw=self.lw, alpha=self.alpha))
          if self.vertical:
            xlim = ax.get_xlim()
            if xlim[0] < event.xdata < xlim[1]:
              self.vls.append(ax.axvline(event.xdata, color=self.color, lw=self.lw, alpha=self.alpha))

      self.fig.canvas.draw()
