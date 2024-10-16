import SwiftUI

struct GrowingTextInputView: View {
  init(text: Binding<String?>, placeholder: String?) {
    self._text = text
    self.placeholder = placeholder
  }

  @Binding var text: String?
  @State var focused: Bool = false
  @State var contentHeight: CGFloat = 0

  let placeholder: String?
  let minHeight: CGFloat = 50
  let maxHeight: CGFloat = 200

  var countedHeight: CGFloat {
    min(max(minHeight, contentHeight), maxHeight) + 20
  }

  var body: some View {
    ZStack(alignment: .topLeading) {
      Color.white
      ZStack(alignment: .topLeading) {
        TextViewWrapper(text: $text, focused: $focused, contentHeight: $contentHeight)
              .padding(10)
              .background(Color.gray.opacity(0.1))
        placeholderView
              .padding(20)
      }
//      .padding(.horizontal, 4)
    }.frame(height: countedHeight)
  }

  var placeholderView: some View {
    ViewBuilder.buildIf(
      showPlaceholder ?
        placeholder.map {
          Text($0)
            .foregroundColor(.gray)
            .font(.system(size: 16))
            .padding(.vertical, 8)
            .padding(.horizontal, 4)
        } : nil
    )
  }

    var showPlaceholder: Bool {
        !focused && (text ?? "").isEmpty
    }
}

#if DEBUG
struct GrowingTextInputView_Previews: PreviewProvider {
  @State static var text: String?

  static var previews: some View {
    GrowingTextInputView(
      text: $text,
      placeholder: "Placeholder"
    ).cornerRadius(10)
  }
}
#endif
