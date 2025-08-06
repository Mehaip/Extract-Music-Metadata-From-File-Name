# Genius Audio Parser

A Python script that automatically identifies and organizes your music collection by extracting metadata from audio filenames using the Genius API.

## Problem It Solves

YouTube songs often follow inconsistent naming formats:

- `artistName - title`
- `title - artistName`
- `title - artistName (official)`
- `title - artistName (music video)`
- `Song Name (Official Audio) - YouTube`
- `Artist - Song (128kbit_AAC)`

This script cleans these filenames, searches the Genius API for proper metadata, and organizes everything in a structured format.

## Features

- 📊 **Multiple output formats** - CSV and JSON exports
- 📁 **Batch processing** - Handles entire folders of audio files

## Supported Audio Formats

- MP3
- FLAC
- M4A/MP4
- WAV
- AAC
- OGG
- WMA
- OPUS