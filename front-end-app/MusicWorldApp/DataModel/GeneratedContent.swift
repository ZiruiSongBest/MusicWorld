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
    var title: String
    var image: Data?
    @Relationship(deleteRule: .cascade) var items: [Item] = []
    var generatedAudioData: [Data] = []
    var desc: String = ""
    
    init(id: UUID = UUID(), prompt: String, title: String) {
        self.id = id
        self.prompt = prompt
        self.title = title
    }
    
    func addItem(_ item: Item) {
        items.append(item)
    }
    
    func addGeneratedAudio(_ audioData: Data) {
        generatedAudioData.append(audioData)
    }
}
