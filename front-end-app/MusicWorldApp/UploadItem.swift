//
//  UploadItem.swift
//  MusicWorldApp
//
//  Created by Dylan on 16/10/2024.
//

import Foundation
import SwiftData

@Model
class Item: Identifiable {
    var id = UUID()
    var title: String
    var duration: String
    var content: String
    var type: ItemType
    
    init(id: UUID = UUID(), title: String, duration: String, content: String, type: ItemType) {
        self.id = id
        self.title = title
        self.duration = duration
        self.content = content
        self.type = type
    }
    
    enum ItemType: String, Codable {
        case audio, file, image
    }
    
    func saveContentToFile() {
        let fileURL = getDocumentsDirectory().appendingPathComponent("\(id).txt")
        do {
            try content.write(to: fileURL, atomically: true, encoding: .utf8)
            print("File saved successfully at \(fileURL)")
        } catch {
            print("Failed to save file: \(error.localizedDescription)")
        }
    }
    
    func loadContentFromFile() {
        let fileURL = getDocumentsDirectory().appendingPathComponent("\(id).txt")
        let accessing = fileURL.startAccessingSecurityScopedResource()
        defer {
            if accessing {
                fileURL.stopAccessingSecurityScopedResource()
            }
        }
        
        do {
            content = try String(contentsOf: fileURL, encoding: .utf8)
            print("File loaded successfully from \(fileURL)")
        } catch {
            print("Failed to load file: \(error.localizedDescription)")
        }
    }
    
    // Helper method to get the documents directory
    private func getDocumentsDirectory() -> URL {
        return FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
    }
}
