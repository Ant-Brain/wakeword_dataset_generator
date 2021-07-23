import matplotlib.pyplot as plt
import torch
import torchaudio
import time 

def plot_specgram(waveform, sample_rate, title="Spectrogram", xlim=None):
  #waveform = waveform.numpy()

  num_channels, num_frames = waveform.shape
  time_axis = torch.arange(0, num_frames) / sample_rate

  figure, axes = plt.subplots(num_channels, 1)
  if num_channels == 1:
    axes = [axes]
  for c in range(num_channels):
    s = time.time()
    axes[c].specgram(waveform[c], Fs=sample_rate)
    print(time.time()-s)
    if num_channels > 1:
      axes[c].set_ylabel(f'Channel {c+1}')
    if xlim:
      axes[c].set_xlim(xlim)
  figure.suptitle(title)
  plt.show(block=False)


samples,sample_rate = torchaudio.load("./noise_files/TrafficSamples/test.wav")
transform = torchaudio.transforms.Resample(orig_freq=sample_rate,new_freq=16000)

samples_2 = transform(samples).numpy()[:16000]
print(samples.shape)
plot_specgram(samples,16000,title="ok")
input("waiting")
