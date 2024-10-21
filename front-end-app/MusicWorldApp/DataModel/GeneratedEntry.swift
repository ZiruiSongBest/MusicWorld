//
//  GeneratedContent.swift
//  MusicWorldApp
//
//  Created by Dylan on 17/10/2024.
//

import Foundation
import SwiftData

@Model
final class GeneratedEntry: Identifiable {
    var id: UUID
    var prompt: String
    var title: String = ""
    var image: Data?
    @Relationship(deleteRule: .cascade) var items: [Item] = []
    var generatedAudioData: [Data] = []
    var desc: String = ""
    var theme: String = ""
    var generatedDate: Date
    
    init(id: UUID = UUID(), prompt: String) {
        self.id = id
        self.prompt = prompt
        self.generatedDate = Date()
//        self.title = title
//        self.theme = theme
    }
    
    func addItem(_ item: Item) {
        items.append(item)
    }
    
    func addGeneratedAudio(_ audioData: Data) {
        generatedAudioData.append(audioData)
    }
    
    func setDetails(title: String, description: String, theme: String) {
        self.title = title
        self.desc = description
        self.theme = theme
    }
}
