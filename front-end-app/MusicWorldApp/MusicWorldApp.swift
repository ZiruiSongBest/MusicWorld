//
//  MusicWorldAppApp.swift
//  MusicWorldApp
//
//  Created by Dylan on 16/10/2024.
//

import SwiftUI
import SwiftData

@main
struct MusicWorldApp: App {
    let sharedModelContainer: ModelContainer

    init() {
        do {
            let schema = Schema([
                GeneratedEntry.self,
                Item.self
            ])
            let modelConfiguration = ModelConfiguration(schema: schema, isStoredInMemoryOnly: false)
            sharedModelContainer = try ModelContainer(for: schema, configurations: [modelConfiguration])
        } catch {
            fatalError("Could not initialize ModelContainer: \(error)")
        }
    }

    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(sharedModelContainer)
    }
}
