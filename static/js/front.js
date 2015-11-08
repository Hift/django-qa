


		/**
		 * add tag to modal, render tagItem base on in put tag
		 */
		jQuery(function(tag) {
			this.tag_list = this.jQuery('ul.tags-list');
			var duplicates = this.tag_list.find('input[type=hidden][value="' + tag + '"]'),
				count = this.tag_list.find('li');
			if (duplicates.length == 0 && tag != '' && count.length < 5) {
				var data = {
					'name': tag
				};
				var tagView = new Views.TagItem({
					model: new Backbone.Model(data)
				});
				this.tag_list.append(tagView.render().$el);
				$('input#question_tags').val('').css('border', '1px solid #dadfea');
			}
		});

		/**
		 * catch event user enter in tax input, call function addTag to render tag item
		 */
		jQuery(function(event) {
			var val = $(event.currentTarget).val();
			console.log('keypress');
			if (event.which == 13) {
				/**
				 * check current user cap can add_tag or not
				 */
				var caps = currentUser.cap;
				if (typeof caps['create_tag'] === 'undefined' && $.inArray(val, this.tags) == -1) {
					this.$('#question_tags').popover({
						content: this.$('#add_tag_text').val(),
						container: '#modal_submit_questions'
					});
					return false;
				}
				/**
				 * add tag
				 */
				this.addTag(val);
			}
			return event.which != 13;
		});


