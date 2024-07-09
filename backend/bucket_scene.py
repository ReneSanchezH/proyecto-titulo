from manim import *

class BucketScene(Scene):
    def construct(self):
        # Title
        title = Text("Uso de buckets").to_edge(UP)
        self.play(Write(title))
        
        # Number to be sorted
        number = Text("816")
        number.next_to(title, DOWN, buff=1)
        self.play(Write(number))
        
        # Buckets
        buckets = VGroup(
            Square().set_height(1).move_to(2 * LEFT + 2 * DOWN),
            Square().set_height(1).move_to(0 * LEFT + 2 * DOWN),
            Square().set_height(1).move_to(2 * RIGHT + 2 * DOWN),
        )
        bucket_labels = VGroup(
            Text("6").next_to(buckets[0], DOWN),
            Text("8").next_to(buckets[1], DOWN),
            Text("1").next_to(buckets[2], DOWN),
        )
        
        self.play(LaggedStart(*[Create(bucket) for bucket in buckets], lag_ratio=0.5))
        self.play(LaggedStart(*[Write(label) for label in bucket_labels], lag_ratio=0.5))
        
        # Explanation for each digit
        digits = [("unidades", "6", buckets[0]), ("decenas", "1", buckets[2]), ("centenas", "8", buckets[1])]
        
        for place, digit, bucket in digits:
            self.explain_digit(number, place, digit, bucket)
        
    def explain_digit(self, number, place, digit, bucket):
        digit_text = Text(f"Dígito en {place}: {digit}")
        digit_text.next_to(number, DOWN, buff=0.5)
        
        self.play(Write(digit_text))
        
        digit_highlight = SurroundingRectangle(number, color=YELLOW)
        self.play(Create(digit_highlight))
        
        bucket_highlight = SurroundingRectangle(bucket, color=YELLOW)
        self.play(Create(bucket_highlight))
        
        self.play(number.animate.move_to(bucket.get_center()))
        self.play(number.animate.move_to(digit_highlight.get_center()))
        
        self.play(FadeOut(digit_highlight), FadeOut(bucket_highlight), FadeOut(digit_text))
