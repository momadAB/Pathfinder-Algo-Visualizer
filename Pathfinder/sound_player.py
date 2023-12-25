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
    # Base frequency range determined by x-coordinate (e.g., 220 to 440 Hz)
    base_frequency = np.interp(x, [0, grid_width], [110, 330])

    # Additional frequency variation determined by y-coordinate (e.g., +/- 20 Hz)
    frequency_variation = np.interp(y, [0, grid_height], [-20, 20])

    # Final frequency is the sum of base frequency and variation
    frequency = base_frequency + frequency_variation

    # print(f"Creating sound with frequency: {frequency} Hz for position: ({x}, {y})")  # Debugging line

    # Create an array that represents the sound wave
    sample_rate = 44100
    duration = 0.1  # shorter duration for a quick sound effect
    t = np.linspace(0, duration, int(sample_rate * duration))
    wave = np.sin(2 * np.pi * frequency * t)  # Sine wave formula

    # Ensure it's in 16-bit to be compatible with Pygame sound array
    wave = np.array(wave * 32767, 'int16')

    # Create a stereo sound by duplicating the wave into two channels
    stereo_wave = np.zeros((wave.size, 2), dtype=np.int16)  # initialize a 2D array for stereo
    stereo_wave[:, 0] = wave  # left channel
    stereo_wave[:, 1] = wave  # right channel

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

