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
    
    // Key for storing the network address in UserDefaults
    private let networkAddressKey = "NetworkAddress"
    
    // Property to get and set the network address
    var networkAddress: String {
        get {
            return UserDefaults.standard.string(forKey: networkAddressKey) ?? ""
        }
        set {
            UserDefaults.standard.set(newValue, forKey: networkAddressKey)
        }
    }
    
    func generateAudio(textPrompt: String, items: [Item], completion: @escaping (Data?, String?, Error?) -> Void) {
        guard !networkAddress.isEmpty,
              let url = URL(string: networkAddress + "/generate") else {
            completion(nil, nil, NSError(domain: "Invalid URL", code: 0, userInfo: nil))
            return
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        let boundary = UUID().uuidString
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
        
        // Add the network address to the request headers
        request.setValue(networkAddress, forHTTPHeaderField: "X-Network-Address")
        
        let formData = createFormData(textPrompt: textPrompt, items: items, boundary: boundary)
        request.httpBody = formData
        
        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                print("Error: \(error.localizedDescription)")
                completion(nil, nil, error)
                return
            }
            
            if let httpResponse = response as? HTTPURLResponse {
                print("Status Code: \(httpResponse.statusCode)")
                print("Headers: \(httpResponse.allHeaderFields)")
                
                if httpResponse.statusCode != 200 {
                    completion(nil, nil, NSError(domain: "HTTP Error", code: httpResponse.statusCode, userInfo: nil))
                    return
                }
                
                // Extract the description from the custom header
                let description = httpResponse.allHeaderFields["X-Audio-Description"] as? String
                print("Audio Description: \(description ?? "No description available")")
                
                if let data = data {
                    print("Received audio data of size: \(data.count) bytes")
                    completion(data, description, nil)
                } else {
                    completion(nil, nil, NSError(domain: "No data received", code: 0, userInfo: nil))
                }
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
