//
//  GeneratedContentDetailView.swift
//  MusicWorldApp
//
//  Created by Dylan on 19/10/2024.
//

import SwiftUI


struct GeneratedContentDetailView: View {
    let content: GeneratedContent
    @State private var selectedAudioIndex: Int?
    @State private var isAudioPlayerVisible = false

    var body: some View {
        ZStack {
            List {
                Section(header: Text("Prompt")) {
                    Text(content.prompt)
                }
                
                Section(header: Text("Items")) {
                    ForEach(content.items) { item in
                        ItemView(item: item)
                    }
                }

                Section(header: Text("Description")) {
                    Text(content.desc)
                }
                
                if !content.generatedAudioData.isEmpty {
                    Section(header: Text("Generated Audio")) {
                        ForEach(content.generatedAudioData.indices, id: \.self) { index in
                            Button("Audio \(index + 1)") {
                                toggleAudio(index)
                            }
                        }
                    }
                }
                
                // Add some empty space at the bottom of the list
                Section {
                    Color.clear.frame(height: 220)
                }
                .listRowBackground(Color.clear)
            }
            .listStyle(InsetGroupedListStyle())
            
            VStack {
                Spacer()
                if let index = selectedAudioIndex {
                    AudioPlayerView(audioData: content.generatedAudioData[index])
                        .frame(height: 200)
                        .background(Color(UIColor.systemBackground))
                        .cornerRadius(15)
                        .shadow(radius: 5)
                        .padding(.horizontal)
                        .padding(.bottom, 10)
                        .opacity(isAudioPlayerVisible ? 1 : 0)
                        .offset(y: isAudioPlayerVisible ? 0 : 50)
                        .animation(.easeInOut(duration: 0.3), value: isAudioPlayerVisible)
                }
            }
        }
        .navigationTitle(content.title)
        .background(Color(UIColor.systemGroupedBackground).edgesIgnoringSafeArea(.all))
    }

    private func toggleAudio(_ index: Int) {
        if selectedAudioIndex == index {
            // If the same audio is tapped, hide it
            withAnimation {
                isAudioPlayerVisible = false
            }
            // Delay the resetting of selectedAudioIndex to allow the hide animation to complete
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.3) {
                selectedAudioIndex = nil
            }
        } else {
            // If a different audio is tapped, show it
            selectedAudioIndex = index
            withAnimation {
                isAudioPlayerVisible = true
            }
        }
    }
}

//#Preview {
//    GeneratedContentDetailView()
//}
