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
    
    var body: some View {
        VStack {
            Text("Audio Player")
                .font(.largeTitle)
                .padding()
            
            Button(action: {
                togglePlayback()
            }) {
                Text(isPlaying ? "Pause" : "Play")
                    .foregroundColor(.white)
                    .padding()
                    .background(Color.blue)
                    .cornerRadius(10)
            }
            
            Slider(value: $currentTime, in: 0...duration, onEditingChanged: sliderEditingChanged)
                .padding()
            
            Text("Current Time: \(formatTime(currentTime)) / \(formatTime(duration))")
                .padding()
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
}
