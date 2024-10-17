//
//  NetworkManager.swift
//  MusicWorldApp
//
//  Created by Dylan on 17/10/2024.
//

import Foundation

class NetworkManager {
    static let shared = NetworkManager()
    
    private init() {}
    
    func generateAudio(textPrompt: String, items: [Item], completion: @escaping (Data?, Error?) -> Void) {
        guard let url = URL(string: "http://localhost:8000/generate") else {
            completion(nil, NSError(domain: "Invalid URL", code: 0, userInfo: nil))
            return
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        let boundary = UUID().uuidString
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
        
        let formData = createFormData(textPrompt: textPrompt, items: items, boundary: boundary)
        request.httpBody = formData
        
        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                print("Error: \(error.localizedDescription)")
                completion(nil, error)
                return
            }
            
            if let httpResponse = response as? HTTPURLResponse {
                print("Status Code: \(httpResponse.statusCode)")
                print("Headers: \(httpResponse.allHeaderFields)")
                
                if httpResponse.statusCode != 200 {
                    completion(nil, NSError(domain: "HTTP Error", code: httpResponse.statusCode, userInfo: nil))
                    return
                }
            }
            
            if let data = data {
                print("Received audio data of size: \(data.count) bytes")
                completion(data, nil)
            } else {
                completion(nil, NSError(domain: "No data received", code: 0, userInfo: nil))
            }
        }
        
        task.resume()
    }
    
    private func createFormData(textPrompt: String, items: [Item], boundary: String) -> Data {
        var body = Data()
        
        // Append text prompt to form data
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"text_prompt\"\r\n\r\n".data(using: .utf8)!)
        body.append("\(textPrompt)\r\n".data(using: .utf8)!)
        
        // Group items by type
        let textItems = items.filter { $0.type == .file }
        let audioItems = items.filter { $0.type == .audio }
        let imageItems = items.filter { $0.type == .image }
        let videoItems = items.filter { $0.type == .video }
        
        // Append text files
        appendFiles(to: &body, items: textItems, fieldName: "text_files", mimeType: "text/plain", fileExtension: "txt", boundary: boundary)
        
        // Append audio files
        appendFiles(to: &body, items: audioItems, fieldName: "audio", mimeType: "audio/mpeg", fileExtension: "mp3", boundary: boundary)
        
        // Append image files
        appendFiles(to: &body, items: imageItems, fieldName: "image", mimeType: "image/jpeg", fileExtension: "jpg", boundary: boundary)
        
        // Append video files
        appendFiles(to: &body, items: videoItems, fieldName: "video", mimeType: "video/mp4", fileExtension: "mp4", boundary: boundary)
        
        // Closing boundary
        body.append("--\(boundary)--\r\n".data(using: .utf8)!)
        
        return body
    }
    
    private func appendFiles(to body: inout Data, items: [Item], fieldName: String, mimeType: String, fileExtension: String, boundary: String) {
        for (index, item) in items.enumerated() {
            body.append("--\(boundary)\r\n".data(using: .utf8)!)
            body.append("Content-Disposition: form-data; name=\"\(fieldName)\"; filename=\"\(fieldName)_\(index+1).\(fileExtension)\"\r\n".data(using: .utf8)!)
            body.append("Content-Type: \(mimeType)\r\n\r\n".data(using: .utf8)!)
            body.append(item.content)
            body.append("\r\n".data(using: .utf8)!)
            
            print("Sending file: \(fieldName)_\(index+1).\(fileExtension)")
            print("File size: \(item.content.count) bytes")
            print("MIME type: \(mimeType)")
        }
    }
}
