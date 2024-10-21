//
//  ItemView.swift
//  MusicWorldApp
//
//  Created by Dylan on 20/10/2024.
//

import SwiftUI
import AVKit


struct ItemView: View {
    let item: Item
    @Binding var isShowingPreview: Bool

    var body: some View {
        ZStack {
            HStack {
                VStack(alignment: .leading) {
                    Text(item.title)
                        .font(.headline)
                    Text(item.duration)
                        .font(.subheadline)
                        .foregroundColor(.gray)
                }
                Spacer()
                Image(systemName: iconName)
                    .resizable()
                    .frame(width: 30, height: 30)
            }
            .padding()
        }
        .listRowInsets(EdgeInsets())
        .padding(.vertical, 5)
        .contextMenu {
            Button(action: {
                isShowingPreview = true
            }) {
                Label("Preview", systemImage: "eye")
            }
            // ... existing delete button ...
        }
        .sheet(isPresented: $isShowingPreview) {
            PreviewView(item: item)
        }
    }

    var iconName: String {
        switch item.type {
        case .audio:
            return "play.circle"
        case .file:
            return "doc.circle"
        case .image:
            return "photo.circle"
        case .video:
            return "video.circle"
        }
    }
}


#Preview {
//    ItemView()
}


struct PreviewView: View {
    let item: Item

    var body: some View {
        Group {
            switch item.type {
            case .audio:
                AudioPreview(audioData: item.content)
            case .file:
                TextPreview(text: String(data: item.content, encoding: .utf8) ?? "Unable to load text")
            case .image:
                ImagePreview(imageData: item.content)
            case .video:
                VideoPreview(videoData: item.content)
            }
        }
    }
}

struct AudioPreview: View {
    let audioData: Data
    @State private var player: AVAudioPlayer?

    var body: some View {
        VStack {
            Text("Audio Preview")
            Button("Play") {
                playAudio()
            }
        }
        .onAppear {
            setupAudioPlayer()
        }
    }

    private func setupAudioPlayer() {
        do {
            player = try AVAudioPlayer(data: audioData)
        } catch {
            print("Error setting up audio player: \(error)")
        }
    }

    private func playAudio() {
        player?.play()
    }
}

struct TextPreview: View {
    let text: String

    var body: some View {
        ScrollView {
            Text(text)
                .padding()
        }
    }
}

struct ImagePreview: View {
    let imageData: Data

    var body: some View {
        if let uiImage = UIImage(data: imageData) {
            Image(uiImage: uiImage)
                .resizable()
                .scaledToFit()
        } else {
            Text("Unable to load image")
        }
    }
}

struct VideoPreview: View {
    let videoData: Data
    @State private var player: AVPlayer?

    var body: some View {
        VStack {
            if let player = player {
                VideoPlayer(player: player)
            } else {
                Text("Unable to load video")
            }
        }
        .onAppear {
            setupVideoPlayer()
        }
    }

    private func setupVideoPlayer() {
        let documentsPath = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
        let tempURL = documentsPath.appendingPathComponent("tempVideo.mp4")
        
        do {
            try videoData.write(to: tempURL)
            player = AVPlayer(url: tempURL)
        } catch {
            print("Error setting up video player: \(error)")
        }
    }
}
