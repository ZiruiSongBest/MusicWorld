import SwiftUI
import AVFoundation

struct AudioPlayerView: View {
    let audioData: Data
    @State private var audioPlayer: AVPlayer?
    @State private var playerItem: AVPlayerItem?
    @State private var isPlaying = false
    @State private var currentTime: Double = 0.0
    @State private var duration: Double = 0.0
    @State private var timeObserverToken: Any?
    @State private var volume: Float = 1.0
    @State private var isSeeking = false
    @State private var showVolumeSlider = false
    
    var body: some View {
        ZStack {
            VStack(spacing: 20) {
                
                // Time labels and volume button
                if !showVolumeSlider {
                    HStack {
                        Text(formatTime(currentTime))
                        Slider(value: $currentTime, in: 0...duration, onEditingChanged: sliderEditingChanged)
                            .accentColor(.blue)
                        Text(formatTime(duration))
                        Button(action: toggleVolumeSlider) {
                            Image(systemName: "speaker.wave.2.fill")
                                .foregroundColor(.blue)
                                .font(.title3)
                        }
                     }
                    .font(.caption)
                    .padding(.horizontal)
                }
                
                
                // Volume slider (conditionally visible)
                if showVolumeSlider {
                    HStack {
                        HStack {
                            Image(systemName: "speaker.fill")
                                .foregroundColor(.gray)
                            Slider(value: $volume, in: 0...1, onEditingChanged: volumeChanged)
                                .accentColor(.blue)
                                .frame(width: 200)
                            Image(systemName: "speaker.wave.3.fill")
                                .foregroundColor(.gray)
                        }
                        .padding(.horizontal, 8)
                        .background(Color.gray.opacity(0.1))
                        .cornerRadius(20)
                        
                        Button(action: toggleVolumeSlider) {
                            Image(systemName: "xmark.circle")
                                .foregroundColor(.gray)
                                .font(.title3)
                        }
                        
                    }
                    .frame(maxWidth: .infinity)
                    .padding(.horizontal)
                    .cornerRadius(10)
                }
                
                // Playback controls
                HStack(spacing: 40) {
                    Button(action: rewindTenSeconds) {
                        Image(systemName: "gobackward.5")
                            .font(.title)
                    }
                    
                    Button(action: togglePlayback) {
                        Image(systemName: isPlaying ? "pause.circle.fill" : "play.circle.fill")
                            .font(.system(size: 60))
                    }
                    
                    Button(action: forwardTenSeconds) {
                        Image(systemName: "goforward.5")
                            .font(.title)
                    }
                }
            }
            // .padding()
            
        }
        .onAppear {
            prepareAudioPlayer()
        }
        .onDisappear {
            if let token = timeObserverToken {
                audioPlayer?.removeTimeObserver(token)
                timeObserverToken = nil
            }
        }
    }
    
    private func prepareAudioPlayer() {
        let tempDirectory = FileManager.default.temporaryDirectory
        let audioFileURL = tempDirectory.appendingPathComponent("receivedAudio.wav")
        
        do {
            try audioData.write(to: audioFileURL)
            playerItem = AVPlayerItem(url: audioFileURL)
            audioPlayer = AVPlayer(playerItem: playerItem)
            
            if let duration = playerItem?.asset.duration {
                self.duration = CMTimeGetSeconds(duration)
            }
            
            addPeriodicTimeObserver()
        } catch {
            print("Error writing audio data to file: \(error)")
        }
    }
    
    private func togglePlayback() {
        guard let player = audioPlayer else { return }
        
        if isPlaying {
            player.pause()
        } else {
            player.play()
        }
        
        isPlaying.toggle()
    }
    
    private func sliderEditingChanged(editingStarted: Bool) {
        guard let player = audioPlayer else { return }
        
        if editingStarted {
            player.pause()
        } else {
            let newTime = CMTime(seconds: currentTime, preferredTimescale: 600)
            player.seek(to: newTime) { _ in
                if self.isPlaying {
                    player.play()
                }
            }
        }
    }
    
    private func addPeriodicTimeObserver() {
        guard let player = audioPlayer else { return }
        
        let interval = CMTime(seconds: 1, preferredTimescale: 600)
        timeObserverToken = player.addPeriodicTimeObserver(forInterval: interval, queue: .main) { time in
            self.currentTime = CMTimeGetSeconds(time)
        }
    }
    
    private func formatTime(_ time: Double) -> String {
        let minutes = Int(time) / 60
        let seconds = Int(time) % 60
        return String(format: "%02d:%02d", minutes, seconds)
    }
    
    private func rewindTenSeconds() {
        seek(by: -5)
    }
    
    private func forwardTenSeconds() {
        seek(by: 5)
    }
    
    private func seek(by seconds: Double) {
        guard let player = audioPlayer else { return }
        let newTime = max(0, min(currentTime + seconds, duration))
        player.seek(to: CMTime(seconds: newTime, preferredTimescale: 600))
    }
    
    private func volumeChanged(editingStarted: Bool) {
        if !editingStarted {
            audioPlayer?.volume = volume
        }
    }
    
    private func toggleVolumeSlider() {
        showVolumeSlider.toggle()
    }
}
