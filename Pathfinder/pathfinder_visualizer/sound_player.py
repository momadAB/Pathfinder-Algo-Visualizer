import numpy as np
import pygame


def create_sweep_sound(node_count, duration=2.0):
    """
    Creates a sound that sweeps from a low to high frequency based on the node count.
    """
    # Map the node count to frequency range
    start_freq = 200  # Frequency for the first node
    end_freq = min(200 + node_count, 330)  # Increase frequency with the node count
    sample_rate = 44100

    # Generate a time array
    t = np.linspace(0, duration, int(sample_rate * duration))

    # Create a frequency sweep
    freq_sweep = np.logspace(np.log10(start_freq), np.log10(end_freq), t.size)

    # Generate the sound wave and normalize
    wave = np.sin(2 * np.pi * freq_sweep * t)
    wave = np.int16(wave / np.max(np.abs(wave)) * 32767)

    # Create stereo sound
    stereo_wave = np.column_stack((wave, wave))

    # Convert to Pygame sound
    return pygame.sndarray.make_sound(stereo_wave)


# Function to create a sound based on x-coordinate
def create_sound(x, y, grid_width, grid_height):
    # Map the coordinates to frequencies
    base_frequency = np.interp(x, [0, grid_width], [110, 330])   # 110 330
    frequency_variation = np.interp(y, [0, grid_height], [-20, 20])
    frequency = base_frequency + frequency_variation

    # Create the sound wave
    sample_rate = 44100
    duration = 0.1
    t = np.linspace(0, duration, int(sample_rate * duration))
    wave = np.sin(2 * np.pi * frequency * t)

    # Apply fade in and fade out
    fade_length = int(sample_rate * 0.01)  # 0.01 seconds fade
    fade_in = np.linspace(0, 1, fade_length)
    fade_out = np.linspace(1, 0, fade_length)
    wave[:fade_length] *= fade_in
    wave[-fade_length:] *= fade_out

    # Ensure the wave is 16-bit and stereo
    wave = np.array(wave * 32767, 'int16')
    stereo_wave = np.zeros((wave.size, 2), dtype=np.int16)
    stereo_wave[:, 0] = wave
    stereo_wave[:, 1] = wave

    return pygame.sndarray.make_sound(stereo_wave)


# Function to play the sound for a rectangle being retraced from the path
def play_sound_for_rect_retrace(rect, grid_width, grid_height, volume):
    sound = create_sound(rect.x, rect.y, grid_width, grid_height)
    sound.set_volume(volume)  # Set volume of the sound object
    sound.play()  # Play the sound


# Function to play the sound for a rectangle
def play_sound_for_rect(rect, grid_width, grid_height, volume):
    sound = create_sound(rect.x, rect.y, grid_width, grid_height)
    sound.set_volume(volume)  # Set volume of the sound object
    sound.play()  # Play the sound

