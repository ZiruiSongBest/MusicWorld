//
//  ContentView.swift
//  MusicWorldApp
//
//  Created by Dylan on 16/10/2024.
//

import SwiftUI
import SwiftData

struct ListGeneratedView: View {
    @Environment(\.modelContext) private var modelContext
    @Query private var generatedContents: [GeneratedContent]

    var body: some View {
        NavigationView {
            List {
                ForEach(generatedContents) { content in
                    NavigationLink(destination: GeneratedContentDetailView(content: content)) {
                        VStack(alignment: .leading) {
                            Text(content.prompt)
                                .font(.headline)
                            Text("Items: \(content.items.count)")
                                .font(.subheadline)
                                .foregroundColor(.secondary)
                        }
                    }
                }
                .onDelete(perform: deleteGeneratedContent)
            }
            .navigationTitle("Generated Content")
            .toolbar {
                EditButton()
            }
        }
    }

    private func deleteGeneratedContent(offsets: IndexSet) {
        withAnimation {
            for index in offsets {
                modelContext.delete(generatedContents[index])
            }
        }
    }
}

struct GeneratedContentDetailView: View {
    let content: GeneratedContent

    var body: some View {
        List {
            Section(header: Text("Prompt")) {
                Text(content.prompt)
            }
            
            Section(header: Text("Items")) {
                ForEach(content.items) { item in
                    ItemView(item: item)
                }
            }
            
            if !content.generatedAudioData.isEmpty {
                Section(header: Text("Generated Audio")) {
                    ForEach(content.generatedAudioData.indices, id: \.self) { index in
                        NavigationLink("Audio \(index + 1)", destination: AudioPlayerView(audioData: content.generatedAudioData[index]))
                    }
                }
            }
        }
        .navigationTitle("Generated Content Details")
    }
}

#Preview {
    ListGeneratedView()
        .modelContainer(for: [GeneratedContent.self, Item.self], inMemory: true)
}
