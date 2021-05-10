
# pythyon3
# Code available at https://github.com/Addd12/adabot
"""Object detection with Raspberry Pi"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import io
import argparse
import time
import re
import numpy as np
import picamera
from annotate import Annotator
from PIL import Image
from tflite_runtime.interpreter import Interpreter

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480


def load_labels(path):
  """Read from coco labels file"""
  with open(path, 'r', encoding='utf-8') as f:
    rows = f.readlines()
    labels = {}
    for row_number, content in enumerate(rows):
      pair = re.split(r'[:\s]+', content.strip(), maxsplit=1)
      if len(pair) == 2 and pair[0].strip().isdigit():
        labels[int(pair[0])] = pair[1].strip()
      else:
        labels[row_number] = pair[0].strip()
  return labels


def set_input_tensor(interpreter, image):
  """Setting the input tensor"""
  tensor_index = interpreter.get_input_details()[0]['index']
  input_tensor = interpreter.tensor(tensor_index)()[0]
  input_tensor[:, :] = image


def get_output_tensor(interpreter, index):
  """Outputs the tensor at the given index"""
  output = interpreter.get_output_details()[index]
  tensor = np.squeeze(interpreter.get_tensor(output['index']))
  return tensor


def detect_objects(interpreter, image, threshold):
  """Get the results of detection"""
  set_input_tensor(interpreter, image)
  interpreter.invoke()

  # output details
  boundary = get_output_tensor(interpreter, 0)
  classes = get_output_tensor(interpreter, 1)
  score = get_output_tensor(interpreter, 2)
  count = int(get_output_tensor(interpreter, 3))

  results = []
  for i in range(count):
    if score[i] >= threshold:
      result = {
          'bounding_box': boundary[i],
          'class_id': classes[i],
          'score': score[i]
      }
      results.append(result)
  return results


def annotate_objects(annotator, results, labels):
  """Draw the bounding box"""
  for obj in results:
    ymin, xmin, ymax, xmax = obj['bounding_box'] #coordinates
    xmin = int(xmin * CAMERA_WIDTH)
    xmax = int(xmax * CAMERA_WIDTH)
    ymin = int(ymin * CAMERA_HEIGHT)
    ymax = int(ymax * CAMERA_HEIGHT)

    annotator.bounding_box([xmin, ymin, xmax, ymax]) #display the bounding box and label with score
    annotator.text([xmin, ymin],
                   '%s\n%.2f' % (labels[obj['class_id']], obj['score']))


def main():
  parser = argparse.ArgumentParser(
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument(
      '--model', help='File path of .tflite file.', required=True)
  parser.add_argument(
      '--labels', help='File path of labels file.', required=True)
  parser.add_argument(
      '--threshold',
      help='Score threshold for detected objects.',
      required=False,
      type=float,
      default=0.4)
  args = parser.parse_args()

  labels = load_labels(args.labels)
  interpreter = Interpreter(args.model)
  interpreter.allocate_tensors()
  _, input_height, input_width, _ = interpreter.get_input_details()[0]['shape']

  with picamera.PiCamera(
    # open PI camera
      resolution=(CAMERA_WIDTH, CAMERA_HEIGHT), framerate=30) as camera:
    camera.start_preview()
    try:
      # get real-time data
      stream = io.BytesIO()
      annotator = Annotator(camera)
      for _ in camera.capture_continuous(
          stream, format='jpeg', use_video_port=True):
        stream.seek(0)
        image = Image.open(stream).convert('RGB').resize(
            (input_width, input_height), Image.ANTIALIAS)
        start_time = time.monotonic()
        results = detect_objects(interpreter, image, args.threshold)
        elapsed_ms = (time.monotonic() - start_time) * 1000

        annotator.clear()
        annotate_objects(annotator, results, labels)
        annotator.text([5, 0], '%.1fms' % (elapsed_ms))
        annotator.update()

        stream.seek(0)
        stream.truncate()

    finally:
      camera.stop_preview()


if __name__ == '__main__':
  main()