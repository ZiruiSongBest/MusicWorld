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
                            Text(content.title)
                                .font(.headline)
                            Text(content.desc)
                                .font(.subheadline)
                                .foregroundColor(.secondary)
                            Text("Items: \(content.items.count)")
                                .font(.subheadline)
                                .foregroundColor(.secondary)
                        }
                    }
                }
                .onDelete(perform: deleteGeneratedContent)
            }
            .navigationTitle("Music Lib")
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


#Preview {
    ListGeneratedView()
        .modelContainer(for: [GeneratedContent.self, Item.self], inMemory: true)
}
