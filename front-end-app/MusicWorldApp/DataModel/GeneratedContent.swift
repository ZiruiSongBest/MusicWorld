//
//  GeneratedContent.swift
//  MusicWorldApp
//
//  Created by Dylan on 17/10/2024.
//

import Foundation
import SwiftData

@Model
final class GeneratedContent: Identifiable {
    var id: UUID
    var prompt: String
    @Relationship(deleteRule: .cascade) var items: [Item] = []
    var generatedAudioData: [Data] = []
    
    init(id: UUID = UUID(), prompt: String) {
        self.id = id
        self.prompt = prompt
    }
    
    func addItem(_ item: Item) {
        items.append(item)
    }
    
    func addGeneratedAudio(_ audioData: Data) {
        generatedAudioData.append(audioData)
    }
}
