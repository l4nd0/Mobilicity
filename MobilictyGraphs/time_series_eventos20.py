from pandas import Series, DataFrame
import csv
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from scipy.ndimage.filters import gaussian_filter
import numpy as np
from scipy.signal import find_peaks_cwt
from wordcloud import WordCloud
from matplotlib import style
style.use('ggplot')

from pandas import Series, DataFrame
import random
import time

dicc={}

id = open("top10Evento.txt", 'r')

