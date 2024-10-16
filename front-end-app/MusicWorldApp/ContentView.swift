//
//  ContentView.swift
//  MusicWorldApp
//
//  Created by Dylan on 16/10/2024.
//

import SwiftUI

struct ContentView: View {
    var body: some View {
        TabView {
            GenerateView()
                .tabItem {
                    Image(systemName: "plus.circle.fill")
                    Text("Generate")
                }
            
            ListView()
                .modelContainer(for: Item.self, inMemory: true)
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
    }
}

#Preview {
    ContentView()
}
