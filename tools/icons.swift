import AppKit
func icon(_ px: Int, path: String) {
    let s = CGFloat(px)
    let img = NSImage(size: NSSize(width: s, height: s))
    img.lockFocus()
    NSColor(red: 0x10/255, green: 0x1D/255, blue: 0x33/255, alpha: 1).setFill()
    NSRect(x: 0, y: 0, width: s, height: s).fill()
    let gold = NSColor(red: 0xCF/255, green: 0xAD/255, blue: 0x6B/255, alpha: 1)
    gold.setFill()
    NSRect(x: s*0.18, y: s*0.2, width: s*0.64, height: s*0.045).fill()
    let a: [NSAttributedString.Key: Any] = [.font: NSFont.systemFont(ofSize: s*0.42, weight: .black), .foregroundColor: NSColor.white, .kern: -s*0.01]
    let str = NSAttributedString(string: "GL", attributes: a)
    let sz = str.size()
    str.draw(at: NSPoint(x: (s - sz.width)/2, y: s*0.33))
    img.unlockFocus()
    let rep = NSBitmapImageRep(data: img.tiffRepresentation!)!
    try! rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: path))
}
icon(180, path: CommandLine.arguments[1] + "/apple-touch-icon.png")
icon(192, path: CommandLine.arguments[1] + "/icon-192.png")
icon(512, path: CommandLine.arguments[1] + "/icon-512.png")
