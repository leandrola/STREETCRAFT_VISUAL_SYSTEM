// Capability query only. No VNImageRequestHandler and no recognition execution.
import Vision
import Foundation

let request = VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.revision = VNRecognizeTextRequestRevision3
request.recognitionLanguages = ["en-US"]
request.usesLanguageCorrection = false
print("VISION_REVISION=\(request.revision)")
print("LANGUAGES=\(try request.supportedRecognitionLanguages())")
print("OS=\(ProcessInfo.processInfo.operatingSystemVersionString)")
