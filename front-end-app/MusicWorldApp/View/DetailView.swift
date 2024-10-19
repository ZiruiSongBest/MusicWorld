//
//  GeneratedContentDetailView.swift
//  MusicWorldApp
//
//  Created by Dylan on 19/10/2024.
//

import SwiftUI


struct GeneratedContentDetailView: View {
    let content: GeneratedEntry
    @State private var isShowingPreview = false
    @State private var selectedAudioIndex: Int?
    @State private var isAudioPlayerVisible = false
    @State private var isSharePresented = false

    var body: some View {
        ZStack {
            List {
                Section {
                    VStack(alignment: .leading, spacing: 8) {
                        Text(content.desc)
                            .font(.headline)
                        Text(content.theme)
                            .font(.body)
                            .foregroundColor(.secondary)
                        Text("Generated on \(formattedDate)")
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                    .padding(.vertical, 8)
                }
                
                if content.prompt != "" {
                    Section(header: Text("Prompt")) {
                        Text(content.prompt)
                    }
                }
                
                if !content.items.isEmpty {
                    Section(header: Text("Items")) {
                        ForEach(content.items) { item in
                            ItemView(item: item, isShowingPreview: $isShowingPreview)
                        }
                    }
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
                        .background(
                            Color(UIColor { traitCollection in
                                traitCollection.userInterfaceStyle == .dark ? UIColor.secondarySystemBackground : UIColor.systemBackground
                            })
                        )
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
        .navigationBarItems(trailing: shareButton)
        .background(Color(UIColor.systemGroupedBackground).edgesIgnoringSafeArea(.all))
        .sheet(isPresented: $isSharePresented) {
            if let index = selectedAudioIndex {
                let audioData = content.generatedAudioData[index]
                if let audioFileURL = saveAudioDataToFile(audioData) {
                    ActivityViewController(activityItems: [audioFileURL])
                }
            }
        }
    }

    private var shareButton: some View {
        Button(action: {
            if selectedAudioIndex != nil {
                isSharePresented = true
            }
        }) {
            Image(systemName: "square.and.arrow.up")
        }
        .disabled(selectedAudioIndex == nil)
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

    private var formattedDate: String {
        let formatter = DateFormatter()
        formatter.dateStyle = .medium
        formatter.timeStyle = .short
        return formatter.string(from: content.generatedDate)
    }

    private func saveAudioDataToFile(_ data: Data) -> URL? {
        let tempDirectory = FileManager.default.temporaryDirectory
        let fileURL = tempDirectory.appendingPathComponent("sharedAudio.m4a")
        
        do {
            try data.write(to: fileURL)
            return fileURL
        } catch {
            print("Error saving audio file: \(error)")
            return nil
        }
    }
}

// Add this struct at the bottom of the file
struct ActivityViewController: UIViewControllerRepresentable {
    let activityItems: [Any]
    let applicationActivities: [UIActivity]? = nil

    func makeUIViewController(context: UIViewControllerRepresentableContext<ActivityViewController>) -> UIActivityViewController {
        let controller = UIActivityViewController(activityItems: activityItems, applicationActivities: applicationActivities)
        return controller
    }

    func updateUIViewController(_ uiViewController: UIActivityViewController, context: UIViewControllerRepresentableContext<ActivityViewController>) {}
}

//#Preview {
//    GeneratedContentDetailView()
//}
