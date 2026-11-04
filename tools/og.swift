import AppKit
let w: CGFloat = 1200, h: CGFloat = 630
let img = NSImage(size: NSSize(width: w, height: h))
img.lockFocus()
let navy = NSColor(red: 0x10/255, green: 0x1D/255, blue: 0x33/255, alpha: 1)
let navy2 = NSColor(red: 0x1D/255, green: 0x31/255, blue: 0x53/255, alpha: 1)
let gold = NSColor(red: 0xCF/255, green: 0xAD/255, blue: 0x6B/255, alpha: 1)
NSGradient(starting: navy2, ending: navy)!.draw(in: NSRect(x: 0, y: 0, width: w, height: h), angle: -35)
gold.set(); NSRect(x: 0, y: h-10, width: w, height: 10).fill()
func draw(_ s: String, _ size: CGFloat, _ weight: NSFont.Weight, _ color: NSColor, _ x: CGFloat, _ y: CGFloat, kern: CGFloat = 0) {
    let a: [NSAttributedString.Key: Any] = [.font: NSFont.systemFont(ofSize: size, weight: weight), .foregroundColor: color, .kern: kern]
    NSAttributedString(string: s, attributes: a).draw(at: NSPoint(x: x, y: y))
}
draw("THE GAP LAB", 104, .black, .white, 80, 300, kern: -3)
gold.set(); NSRect(x: 84, y: 270, width: 120, height: 5).fill()
draw("Personalentwicklung, die verbindet.", 52, .bold, NSColor(white: 0.95, alpha: 1), 80, 190)
draw("Verhandlungsstärke, Führungsklarheit und Finanzverständnis.", 30, .regular, NSColor(white: 0.8, alpha: 1), 80, 140)
draw("The Gap Lab GmbH · Altdorf bei Nürnberg · gap-lab.de", 26, .regular, gold, 80, 60)
img.unlockFocus()
let rep = NSBitmapImageRep(data: img.tiffRepresentation!)!
try! rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: CommandLine.arguments[1]))
