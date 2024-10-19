//
//  ContentView.swift
//  MusicWorldApp
//
//  Created by Dylan on 16/10/2024.
//

import SwiftUI
import SwiftData

struct ContentView: View {
    @Environment(\.modelContext) private var modelContext

    var body: some View {
        TabView {
            GenerateView()
                .tabItem {
                    Image(systemName: "plus.circle.fill")
                    Text("Generate")
                }
            
            ListGeneratedView()
                .tabItem {
                    Image(systemName: "music.note.list")
                    Text("List")
                }
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
            .modelContainer(for: [GeneratedEntry.self, Item.self], inMemory: true)
    }
}

#Preview {
    ContentView()
        .modelContainer(for: [GeneratedEntry.self, Item.self], inMemory: true)
}
