// Offline Apple Vision OCR; one batch of local tiles. No network APIs.
import Foundation
import Vision

struct Tile: Decodable { let id: String; let path: String }
struct Detection: Encodable {
    let text: String
    let confidence: Float
    let box: [Double] // normalized xyxy, top-left origin
}
struct Result: Encodable {
    let id: String
    let detections: [Detection]
    let error: String?
}
guard CommandLine.arguments.count == 2 else {
    fatalError("Expected local JSON tile manifest")
}
let input = try Data(contentsOf: URL(fileURLWithPath: CommandLine.arguments[1]))
let tiles = try JSONDecoder().decode([Tile].self, from: input)
var results: [Result] = []
for tile in tiles {
    do {
        let request = VNRecognizeTextRequest()
        request.revision = VNRecognizeTextRequestRevision3
        request.recognitionLevel = .accurate
        request.recognitionLanguages = ["en-US"]
        request.automaticallyDetectsLanguage = false
        request.usesLanguageCorrection = false
        request.minimumTextHeight = 0
        request.customWords = []
        request.usesCPUOnly = true
        let handler = VNImageRequestHandler(url: URL(fileURLWithPath: tile.path), options: [:])
        try handler.perform([request])
        let detections = (request.results ?? []).compactMap { observation -> Detection? in
            guard let top = observation.topCandidates(1).first else { return nil }
            let b = observation.boundingBox
            return Detection(text: top.string, confidence: top.confidence,
                box: [Double(b.minX), Double(1-b.maxY), Double(b.maxX), Double(1-b.minY)])
        }
        results.append(Result(id: tile.id, detections: detections, error: nil))
    } catch {
        results.append(Result(id: tile.id, detections: [], error: String(describing: error)))
    }
}
let encoder = JSONEncoder()
encoder.outputFormatting = [.prettyPrinted, .sortedKeys]
FileHandle.standardOutput.write(try encoder.encode(results))
