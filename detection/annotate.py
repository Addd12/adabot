# pythyon3
# Code available at https://github.com/Addd12/adabot
"""Add annotations to object detection"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from PIL import Image
from PIL import ImageDraw


def _round_up(value, n):
  return n * ((value + (n - 1)) // n)

def _round_buffer_dims(dims):
  width, height = dims
  return _round_up(width, 32), _round_up(height, 16)

class Annotator:
  """Manage annotations"""
  def __init__(self, camera, default_color=None):
    self._camera = camera
    self._dims = camera.resolution
    self._buffer_dims = _round_buffer_dims(self._dims)
    self._buffer = Image.new('RGBA', self._buffer_dims)
    self._overlay = None
    self._draw = ImageDraw.Draw(self._buffer)
    self._default_color = default_color or (0xFF, 0, 0, 0xFF)

  def update(self):
    temp_overlay = self._camera.add_overlay(
        self._buffer.tobytes(), format='rgba', layer=3, size=self._buffer_dims)
    if self._overlay is not None:
      self._camera.remove_overlay(self._overlay)
    self._overlay = temp_overlay
    self._overlay.update(self._buffer.tobytes())

  def clear(self):
    self._draw.rectangle((0, 0) + self._dims, fill=(0, 0, 0, 0x00))

  def bounding_box(self, rect, outline=None, fill=None):
    """Draw bounding box"""
    outline = outline or self._default_color
    self._draw.rectangle(rect, fill=fill, outline=outline)

  def text(self, location, text, color=None):
    """Display text at the correct location"""
    color = color or self._default_color
    self._draw.text(location, text, fill=color)