import SwiftUI
import UniformTypeIdentifiers
import AVFoundation
import PhotosUI
import SwiftData

struct GenerateView: View {
    @State private var selectedTab = 0
    @State var text: String?
    @State private var instructionPrompt = ""
    @State private var isEditing = false
    @State private var items: [Item] = [
//        Item(title: "Twelve Carat Toothache", duration: "5min", content: "", type: .audio),
//        Item(title: "Background Audio 1", duration: "15min", content: "", type: .audio),
//        Item(title: "Project Report", duration: "10 pages", content: "", type: .file),
        //        Item(title: "Vacation Photo", duration: "2.5 MB", content: "", type: .image)
    ]
    @State private var isShowingDocumentPicker = false
    @State private var selectedFileType: UTType = .audio
    @State private var isImporting = false
    @State private var audioPlayer: AVPlayer?
    @State private var audioData: Data?
    @State private var isShowingAudioPlayer = false
    @State private var isInputting = false
    @State private var isShowingImageSourcePicker = false
    @State private var isShowingPhotolib = false
    @State private var selectedItem: PhotosPickerItem?
    @State private var selectedImage: UIImage?
    @State private var isGenerating = false
    @State private var generationStatus = ""
    @State private var showErrorAlert = false
    @State private var errorMessage = ""
    @Environment(\.modelContext) private var modelContext
    @State private var currentGeneratedContent: GeneratedContent?
    
    var body: some View {
        NavigationStack {
            VStack(spacing: 20) {
                HStack {
                    Spacer()
                    Image(systemName: "ellipsis")
                        .padding()
                }
                
                iconButtonsRow()
                
                Picker("", selection: $selectedTab) {
                    Text("File").tag(0)
                    Text("Audio").tag(1)
                    Text("Image").tag(2)
                    Text("Video").tag(3)
                }
                .pickerStyle(SegmentedPickerStyle())
                .padding(.horizontal)
                
                ScrollView {
                    VStack {
                        inputSection
                        itemsList
                    }
                }
                .padding(.horizontal)
                
                generateButton
                
                if isGenerating {
                    ProgressView(generationStatus)
                        .padding()
                }
            }
            .padding(10)
            .fileImporter(
                isPresented: $isImporting,
                allowedContentTypes: [selectedFileType]
            ) { result in
                switch result {
                case .success(let file):
                    handleFileImport(url: file)
                case .failure(let error):
                    print("Error importing file: \(error.localizedDescription)")
                }
            }
            .alert("Error", isPresented: $showErrorAlert) {
                Button("OK", role: .cancel) { }
            } message: {
                Text(errorMessage)
            }
            .navigationDestination(isPresented: $isShowingAudioPlayer) {
                AudioPlayerView(audioData: audioData ?? Data())
            }
        }
    }
    
    private var inputSection: some View {
        Group {
            if selectedTab == 0 {
                HStack(alignment: .center) {
                    GrowingTextInputView(text: $text, placeholder: "Message", isInputting: $isInputting)
                        .cornerRadius(10)
                    
                    if isInputting {
                        Button("Done") {
                            UIApplication.shared.sendAction(#selector(UIResponder.resignFirstResponder), to: nil, from: nil, for: nil)
                            isInputting = false
                        }
                    }
                }
                .padding(.horizontal)
            }
        }
    }
    
    private var itemsList: some View {
        Group {
            if filteredItems.isEmpty && selectedTab != 0 {
                Text("No \(selectedTabLabel) selected to upload yet")
                    .foregroundColor(.gray)
                    .padding(.vertical, 200)
            } else {
                LazyVStack(spacing: 10) {
                    ForEach(filteredItems) { item in
                        ItemView(item: item)
                            .background(Color.gray.opacity(0.1))
                            .cornerRadius(10)
                            .contextMenu {
                                Button(action: {
                                    if let index = items.firstIndex(where: { $0.id == item.id }) {
                                        items.remove(at: index)
                                    }
                                }) {
                                    Label("Delete", systemImage: "trash")
                                }
                            }
                    }
                }
                .padding(.horizontal)
            }
        }
    }
    
    private var generateButton: some View {
        Group {
            if !isInputting {
                HStack {
                    if isGenerating {
                        ProgressView()
                            .frame(width: 30, height: 30)
                    } else {
                        Image(systemName: "waveform")
                            .resizable()
                            .aspectRatio(contentMode: .fit)
                            .frame(width: 30, height: 30)
                            .foregroundColor(.blue)
                    }
                    
                    Button(action: {
                        generateAudio()
                    }) {
                        Text(isGenerating ? "Generating..." : "Generate")
                            .foregroundColor(.white)
                            .padding(.horizontal, 20)
                            .padding(.vertical, 10)
                            .background(isGenerating ? Color.gray : Color.blue)
                            .cornerRadius(20)
                    }
                    .disabled(isGenerating)
                    .padding(10)
                }
            }
        }
    }
    
    private func deleteItems(offsets: IndexSet) {
        let filteredOffsets = offsets.map { filteredItems[$0] }
        items.removeAll(where: { item in
            filteredOffsets.contains(where: { $0.id == item.id })
        })
    }
    
    var filteredItems: [Item] {
        let filtered: [Item]
        switch selectedTab {
        case 0:
            filtered = items.filter { $0.type == .file }
        case 1:
            filtered = items.filter { $0.type == .audio }
        case 2:
            filtered = items.filter { $0.type == .image }
        default:
            filtered = items
        }
        // Debug: Print the filtered items
        print("Filtered items: \(filtered)")
        return filtered
    }
    
    var selectedTabLabel: String {
        switch selectedTab {
        case 0:
            return "files"
        case 1:
            return "audio"
        case 2:
            return "images"
        default:
            return "items"
        }
    }
    
    private func handleFileImport(url: URL) {
        let accessing = url.startAccessingSecurityScopedResource()
        defer {
            if accessing {
                url.stopAccessingSecurityScopedResource()
            }
        }
        
        do {
            let filename = url.lastPathComponent
            let fileSize = getFileSize(url: url)
            let itemType = getItemType(for: selectedFileType)
            
            let fileData = try Data(contentsOf: url) // Read as Data for all file types
            
            // Create a new item and save its content to a file
            let newItem = Item(title: filename, duration: fileSize, content: fileData, type: itemType)
            newItem.saveContentToFile() // Save the content to a file
            
            items.append(newItem)
        } catch {
            print("Error handling file: \(error.localizedDescription)")
        }
    }
    
    func getFileSize(url: URL) -> String {
        do {
            let attributes = try FileManager.default.attributesOfItem(atPath: url.path)
            if let fileSize = attributes[.size] as? Int64 {
                return ByteCountFormatter.string(fromByteCount: fileSize, countStyle: .file)
            }
        } catch {
            print("Error getting file size: \(error)")
        }
        return "Unknown size"
    }
    
    func getItemType(for utType: UTType) -> Item.ItemType {
        switch utType {
        case .audio:
            return .audio
        case .image:
            return .image
        default:
            return .file
        }
    }
    
    private func generateAudio() {
        isGenerating = true
        generationStatus = "Preparing request..."
        let textPrompt = text ?? "Default additional text"

        // Create a new GeneratedContent instance
        let newGeneratedContent = GeneratedContent(prompt: textPrompt)
        items.forEach { newGeneratedContent.addItem($0) }

        NetworkManager.shared.generateAudio(textPrompt: textPrompt, items: items) { data, error in
            DispatchQueue.main.async {
                if let error = error {
                    self.isGenerating = false
                    self.errorMessage = "Error generating audio: \(error.localizedDescription)"
                    self.showErrorAlert = true
                    return
                }

                if let data = data {
                    self.generationStatus = "Processing audio..."
                    self.audioData = data

                    // Store the generated audio in the GeneratedContent instance
                    newGeneratedContent.addGeneratedAudio(data)

                    // Save the GeneratedContent to SwiftData
                    self.modelContext.insert(newGeneratedContent)
                    do {
                        try self.modelContext.save()
                        print("GeneratedContent saved successfully")
                    } catch {
                        print("Error saving GeneratedContent: \(error)")
                    }

                    self.isShowingAudioPlayer = true
                    self.isGenerating = false
                } else {
                    self.isGenerating = false
                    self.errorMessage = "No audio data received"
                    self.showErrorAlert = true
                }
            }
        }
    }
    
    private func playAudio(data: Data) {
        let tempDirectory = FileManager.default.temporaryDirectory
        let audioFileURL = tempDirectory.appendingPathComponent("generatedAudio.wav")
        
        do {
            try data.write(to: audioFileURL)
            audioPlayer = AVPlayer(url: audioFileURL)
            audioPlayer?.play()
        } catch {
            print("Error writing audio data to file: \(error)")
        }
    }
    
    private func createFormData(boundary: String) -> Data {
        var body = Data()
        
        // Append text prompt to form data
        let textPrompt = text ?? "Default additional text"
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"text_prompt\"\r\n\r\n".data(using: .utf8)!)
        body.append("\(textPrompt)\r\n".data(using: .utf8)!)
        
        // Iterate over items to find audio, image, and video data
        for item in items {
            switch item.type {
            case .audio, .image:
                let fieldName: String
                let mimeType: String
                let fileExtension: String
                
                switch item.type {
                case .audio:
                    fieldName = "audio"
                    mimeType = "audio/mpeg"
                    fileExtension = "mp3"
                case .image:
                    fieldName = "image"
                    mimeType = "image/jpeg"
                    fileExtension = "jpg"
                 case .video:
                     fieldName = "video"
                     mimeType = "video/mp4"
                     fileExtension = "mp4"
                default:
                    continue
                }
                
                body.append("--\(boundary)\r\n".data(using: .utf8)!)
                body.append("Content-Disposition: form-data; name=\"\(fieldName)\"; filename=\"\(item.title).\(fileExtension)\"\r\n".data(using: .utf8)!)
                body.append("Content-Type: \(mimeType)\r\n\r\n".data(using: .utf8)!)
                body.append(item.content)
                body.append("\r\n".data(using: .utf8)!)
                
                print("Sending file: \(item.title).\(fileExtension)")
                print("File size: \(item.content.count) bytes")
                print("MIME type: \(mimeType)")
                
            default:
                break
            }
        }
        
        // Closing boundary
        body.append("--\(boundary)--\r\n".data(using: .utf8)!)
        
        return body
    }
    
    private func getDocumentsDirectory() -> URL {
        return FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
    }
    
    private func iconButtonsRow() -> some View {
        HStack(spacing: 30) {
            iconButton(icon: "doc.text", color: .blue, label: "File", tab: 0, fileType: .plainText)
            iconButton(icon: "music.note", color: .pink, label: "Audio", tab: 1, fileType: .audio)
            imageIconButton()
            iconButton(icon: "video", color: .green, label: "Video", tab: 3, fileType: .movie)
        }
    }
    
    private func imageIconButton() -> some View {
        IconButton(icon: "photo.on.rectangle", color: .pink, label: "Image") {
            selectedTab = 2
            selectedFileType = .image
            isShowingImageSourcePicker = true
        }
        .confirmationDialog("Choose Image Source", isPresented: $isShowingImageSourcePicker) {
            Button("Photo Library") {
                // This will be handled by PhotosPicker
                isShowingPhotolib = true
            }
            Button("File Import") {
                isImporting = true
            }
        }
        .photosPicker(isPresented: $isShowingPhotolib,
                      selection: $selectedItem,
                      matching: .images)
        .onChange(of: selectedItem) { oldItem, newItem in
            Task {
                if let data = try? await newItem?.loadTransferable(type: Data.self) {
                    if let uiImage = UIImage(data: data) {
                        selectedImage = uiImage
                        let item = Item(title: "Selected Image", duration: "\(data.count) bytes", content: data, type: .image)
                        items.append(item)
                    }
                }
            }
        }
    }

    private func iconButton(icon: String, color: Color, label: String, tab: Int, fileType: UTType) -> some View {
        IconButton(icon: icon, color: color, label: label) {
            selectedTab = tab
            selectedFileType = fileType
            isImporting = true
        }
    }
}

struct IconButton: View {
    let icon: String
    let color: Color
    let label: String
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            VStack {
                Image(systemName: icon)
                    .resizable()
                    .aspectRatio(contentMode: .fit)
                    .frame(width: 30, height: 30)
                    .padding(10)
                    .background(color.opacity(0.2))
                    .clipShape(RoundedRectangle(cornerRadius: 10))
                Text(label)
                    .font(.caption)
            }
        }
        .buttonStyle(PlainButtonStyle())
    }
}

struct ItemView: View {
    let item: Item
    
    var body: some View {
        ZStack {
//            Color.gray.opacity(0.1)
//                .cornerRadius(10)
            HStack {
                VStack(alignment: .leading) {
                    Text(item.title)
                        .font(.headline)
                    Text(item.duration)
                        .font(.subheadline)
                        .foregroundColor(.gray)
                }
                Spacer()
                Image(systemName: iconName)
                    .resizable()
                    .frame(width: 30, height: 30)
            }
            .padding() // Padding for the content inside the item
        }
        .listRowInsets(EdgeInsets()) // Remove default list row insets for a custom look
        .padding(.vertical, 5) // Add padding to avoid items sticking together
    }
    
    var iconName: String {
        switch item.type {
        case .audio:
            return "play.circle"
        case .file:
            return "doc.circle"
        case .image:
            return "photo.circle"
        case .video:
            return "video.circle"
        }
    }
}

// struct GenerateView_Previews: PreviewProvider {
//     static var previews: some View {
//         GenerateView()
//     }
// }
